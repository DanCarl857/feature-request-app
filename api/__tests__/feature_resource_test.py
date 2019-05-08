import os
import datetime
import pytest
from run import create_app
from models.Model import db, Feature

app = None

@pytest.fixture()
def client():
    test_config = {
        'TESTING': True,
        'DEBUG': True
    }
    global app
    app = create_app("config", test_config=test_config)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(app.instance_path, 'test.db')
    with app.app_context():
        db.drop_all()
        db.create_all()

        feature = Feature(
            title='Test Title',
            description='Test Description',
            client='Client A',
            product_area='Billing',
            priority=1,
            target_date=datetime.datetime.utcnow().date()
        )
        try:
            db.session.add(feature)
            db.session.commit()
        except:
            db.session.rollback()
            raise
        finally:
            db.session.close()
    client = app.test_client()

    yield client


# Sucesses
def test_get_feature_by_ID(client):
    """Should get feature with given ID"""
    res = client.get('/api/v1/features/1')
    assert(res.status_code == 200)

    feature = res.json['data']
    assert(feature['title'] == 'Test Title')
    assert(feature['description'] == 'Test Description')
    assert(feature['id'] == 1)

def test_get_features(client):
    """Get all features from database"""
    res = client.get('/api/v1/features')
    assert(res.status_code == 200)

    features = res.json['data']
    assert(len(features) == 1)

def test_delete_feature(client):
    """Should delete a feature"""
    # Check if feature is present
    with app.app_context():
        feature = Feature.query.get(1)
        assert(feature is not None)

    res = client.delete('/api/v1/features/1')
    assert(res.status_code == 204)

    # Check if feature was deleted
    with app.app_context():
        feature = Feature.query.get(1)
        assert(feature is None)

def test_create_feature_order_priority_for_client(client):
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 1)
        assert(tickets[0].priority == 1)

    # Let's create a new feature for client A with priority 1.
    res = client.post('/api/tickets', json={
        'title': 'New Feature',
        'description': 'New Feature',
        'client': 'Client A',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-09-09'
    })

    assert(res.status_code == 201)

    created = res.json['data']
    assert(created['title'] == 'New Feature')

    # Existing feature's priority should now be 2
    with app.app_context():
        feature = Feature.query.get(1)
        assert(feature.priority == 2)

def test_update_feature_request(client):
    with app.app_context():
        feature = Feature.query.get(1)
        assert(feature.title == 'Test Title')

    res = client.put('/api/v1/features', json={
        'id': 1,
        'title': 'Now Test 2',
        'description': 'Some feature',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Billing',
        'target_date': '2019-08-09'
    })

    assert(res.status_code == 200)

    with app.app_context():
        feature = Feature.query.get(1)
        assert(feature.title == 'Now Test 2')
    
def test_unique_feature_title(client):
    # Let's add one more feature
    client.post('/api/v1/features', json={
        'title': 'My feature request',
        'description': 'Some feature request',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Billing',
        'target_date': '2019-08-09'
    })

    # Check number of tickets in system. Should be 2
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 2)

    # Now let's try to edit the title of 'Some feature' to 'Test'
    res = client.put('/api/v1/features', json={
        'id': 2,
        'title': 'Test Title',
        'description': 'Some feature',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Billing',
        'target_date': '2019-08-09'
    })

    assert(res.status_code == 400)

    res_message = res.json['message']
    assert(res_message == 'A feature with similar title already exists')

#Failures
def test_get_feature_by_ID_failure(client):
    """Should return 404 if feature is doesn't exist"""
    # first confirm feature doesn't exist
    with app.app_context():
        feature = Feature.query.get(4)
        assert(feature is None)

    # now try to get feature via REST
    res = client.get('/api/v1/feature/100')
    assert(res.status_code == 404)

    res_message = res.json['message']
    assert(res_message == 'Feature does not exist')

def test_delete_feature_failure(client):
    """Should return 404 when deleting a feature that doesn't exist"""
    # First we make sure feature with ID 4 doesn't exist
    with app.app_context():
        feature = Feature.query.get(4)
        assert(feature is None)

    # Now try to delete feature with ID 4
    res = client.delete('/api/v1/features/100')
    assert(res.status_code == 404)

    res_message = res.json['message']
    assert(res_message == 'Feature does not exist')

def test_create_feature_failure(client):
    """Should create feature if it doesn't exist"""
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 1)

    res = client.post('/api/v1/features', json={
        'title': 'New Feature',
        'description': 'New Feature',
        'client': 'Client A',
        'priority': 1,
        'product_area': 'Billing',
        'target_date': '2019-09-09'
    })

    assert(res.status_code == 201)

    created = res.json['data']
    assert(created['title'] == 'New Feature')

    # Verify if feature was created by checking number of features. Should be 2
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 2)

def test_feature_already_exists_on_creation(client):
    """Should return 400 when trying to create a feature that already exists"""
    # Confirm feature with title: Test Title exists
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 1)
        assert(tickets[0].title == 'Test Title')

    # Now let's try to add a feature with title 'Test
    res = client.post('/api/tickets', json={
        'title': 'Test Title',
        'description': 'New Feature',
        'client': 'Client B',
        'priority': 1,
        'product_area': 'Policies',
        'target_date': '2019-09-09'
    })

    print(res)

    assert(res.status_code == 404)

    res_message = res.json['message']
    assert(res_message == 'Feature request already exists')

    # Now let's very that no feature was added
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 1)


def test_no_payload_provided(client):
    """Should return 400 no payload is sent with the request"""
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 1)

    # Make POST request with no payload
    res = client.post('/api/v1/features', json={})

    assert(res.status_code == 400)

    res_message = res.json['message']
    assert(res_message == 'No payload provided')

    # Now let's very that no feature was added
    with app.app_context():
        tickets = Feature.query.all()
        assert(len(tickets) == 1)

def test_no_payload_provided_for_update(client):
    """PUT expects payload to be provided. Return 400 error if payload is not present"""

    res = client.put('/api/v1/features')
    assert(res.status_code == 400)

def test_update_of_nonexistent_feature(client):
    # Confirm feature with ID 100 doesn't exist
    with app.app_context():
        feature = Feature.query.get(100)
        assert(feature is None)

        res = client.put('/api/v1/features', json={
            'id': '100',
            'title': 'Some feature that does not exist',
            'description': 'No body',
            'client': 'Client A',
            'priority': 1,
            'product_area': 'Billing',
            'target_date': '2019-09-09'
        })

        assert(res.status_code == 404)

        res_message = res.json['message']
        assert(res_message == 'Feature does not exist')

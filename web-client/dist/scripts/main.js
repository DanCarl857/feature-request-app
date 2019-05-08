$(document).ready(function() {
    const baseUrl = 'http://127.0.0.1:5000/';

    let table = $('#dtTable').DataTable({
        'processing': true,
        'ajax': {
            'url': baseUrl + 'api/v1/features',
        },
        'columns': [
            {"data": "title"},
            {"data": "description"},
            {"data": "client"},
            {"data": "product_area"},
            {"data": "priority"},
            {"data": "target_date"},
            {
                mRender: function(data, type, row) {
                    return '<a href="#"><span class="glyphicon glyphicon-pencil" data-id="' + row.id + '" id="btnEdit"></span></a> / <a href="#"><span class="glyphicon glyphicon-trash red" data-id="' + row.id + '" id="btnDelete"></span></a>'
                }
            },
        ]
    });

    $('#dtTable').on('click', 'span#btnDelete', function(){
        $('#infoMsg').hide();
        let shouldDelete = confirm('Are you sure you want to delete this feature request?')
        if (shouldDelete) {
            var id = $(this).attr('data-id');
            $.ajax({
                url: baseUrl + 'api/v1/features/' + id,
                type: 'DELETE',
                success: function(result) {
                    table.ajax.reload(null, false);
                }
            })
        }
    });

    $('#toggleModal').click(function () {
        $('#infoMsg').hide();
        $('#featureRequestForm').trigger('reset');
    })

    function getFormData($form) {
        let unindexed_array = $form.serializeArray();
        let indexed_array = {};

        $.map(unindexed_array, function(n, i) {
            indexed_array[n['name']] = n['value']
        });

        return indexed_array;
    }

    function validate(formData) {
        if (formData.title.trim() === '' || formData.description.trim() === '' || formData.client.trim() === '' || formData.productArea.trim() === '' || !formData.targetDate || !formData.priority) {
            return false;
        }
        return true;
    }

    $('#addNewFeatureRequestBtn').click( function() {
        let formData = getFormData($("#featureRequestForm"));
        let isValid = validate(formData);

        // This handles the issue where server returns: 422 (UNPROCESSABLE ENTITY)
        let payload = {
            title: formData.title,
            description: formData.description,
            client: formData.client,
            product_area: formData.productArea,
            priority: formData.priority,
            target_date: formData.targetDate
        }

        if (isValid) {
            $.ajax({
                type: 'POST',
                url: baseUrl + 'api/v1/features',
                data: JSON.stringify(payload),
                success: function(result) {
                    $('#addFeatureRequestModal').modal('hide');
                    table.ajax.reload(null, false);
                    $('#infoMsg').show();
                    $('#featureRequestForm').trigger('reset');
                }
            })
        } else {
            // $('#addErrorMsg').show()
            alert('All fields are required');
        }
    });

    $('#updateFeatureBtn').click( function() {
        $('#infoMsg').hide();
        let formData = getFormData($("#updateFeatureRequestForm"));

        let isValid = validate(formData);

        let payload = {
            id: $('#featureId').val(),
            title: formData.title,
            description: formData.description,
            client: formData.client,
            product_area: formData.productArea,
            priority: formData.priority,
            target_date: formData.targetDate
        }
        
        if (isValid) {
            $.ajax({
                type: 'PUT',
                url: baseUrl + 'api/v1/features',
                data: JSON.stringify(payload),
                success: function(result) {
                    $('#editModal').modal('hide');
                    table.ajax.reload(null, false);
                    $('#infoMsg').show();
                }
            })
        } else {
            alert('All fields are required');
        }
    });

    $('#dtTable').on('click', 'span#btnEdit', function(){
        $('#infoMsg').hide();
        var featureId = $(this).attr('data-id');

        $.get(baseUrl + 'api/v1/features/' + featureId, function(result) {
            var feature = result['data'];
            console.log(feature);
            $('#editTitle').val(feature['title']);
            $('#editDescription').val(feature['description']);
            $('#editClient').val(feature['client']);
            $('#editProductArea').val(feature['product_area']);
            $('#editPriority').val(feature['priority']);
            $('#editTargetDate').val(feature['target_date']);
            $('#featureId').val(feature['id']);

            $('#editModal').modal('show');
        })
    });
});

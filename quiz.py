from cryptography.fernet import Fernet

key = 'TluxwB3fV_GWuLkR1_BzGs1Zk90TYAuhNMZP_0q4WyM='

# Oh no! The code is going over the edge! What are you going to do?
message = b'gAAAAABc0ePWhr1cAJ_PHu6AVa4KC2je_nKTTEoJy7H3CrAjYgzHupF1TNK6zZvnmDfg0dVas6ms0lYsYvFkpoqWTlGWVskK-WkV6ZdC4POOByz5z9eWa0nXWtA3OYOgPIHEBPWPtGA6T8Ffo56cGioV8AHcNPe87ES35D2jdlyqrs6-ZKBR8mfu8V59lKHbyUzq3uc7Umad'

def main():
    f = Fernet(key)
    print(f.decrypt(message))


if __name__ != "__main__":
    main()
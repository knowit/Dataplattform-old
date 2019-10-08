import requests
from airtable import Airtable

# Airtable API settings
airtable_api_key = ""
airtable_base_id = ""
airtable_table_name = ""

# CVPartner API settings
cvpartner_api_key = ""

bio_field_name = "speaker_bio"
image_field_name = "speaker_image"


def make_attachment_obj(image_url, filename):
    """
    This method creates an attachement object for
    airtable attachment column type

    :param image_url: link to picture
    :param filename: what to call the picture
    :return: the image object
    """
    image_object =\
        [
            {
                "url": image_url,
                "filename": filename,
            }
        ]
    return image_object


def get_cvpartner_data(email):
    """
    This method searches for a user on cvpartner based on an email
    and fetches image url and description of the user

    :param email: The email which are searched after
    :return: description and image url if found. else None
    """
    url = f"https://knowit.cvpartner.com/api/v1/users/find?email={email}"
    headers = {'Authorization': 'Token token={}'.format(cvpartner_api_key)}
    try:
        response = requests.get(url, headers=headers).json()

        user_id = response["user_id"]
        default_cv_id = response["default_cv_id"]

        url = f"https://knowit.cvpartner.com/api/v3/cvs/{user_id}/{default_cv_id}"
        response = requests.get(url, headers=headers).json()
        long_description = response["key_qualifications"][0]["long_description"]["no"]

        image_url = response["image"]["url"]
        return long_description, image_url

    except:
        print("No data on "+email+" found at knowit.cvpartner.com")

    return None, None


def main():
    """
    The main method. Initializes airtable object.
    For each record in airtable it fetches corresponding cvpartner data and
    updates the airtable record

    :return: None
    """
    airtable = Airtable(airtable_base_id, airtable_table_name, api_key=airtable_api_key)
    records = airtable.get_all(fields=["email", bio_field_name, image_field_name])

    for record in records:

        # checks if a email is present in the record
        if 'email' not in record['fields']:
            continue

        email = record['fields']['email']
        # ignores non @knowit.no emails
        if not email.endswith("@knowit.no"):
            continue

        # does not update if bio and image_url already exists
        if bio_field_name in record['fields'] and image_field_name in record['fields']:
            print("both filled out")
            continue

        cv_bio, image_url = get_cvpartner_data(email)
        if cv_bio:
            if bio_field_name not in record['fields']:
                print("updating cv")
                fields = {bio_field_name: cv_bio}
                airtable.update(record['id'], fields)
        if image_url:
            if image_field_name not in record['fields']:
                print("updating image url")
                filename = email.split('@', 1)[0]
                image_object = make_attachment_obj(image_url, filename)
                fields = {image_field_name: image_object}
                airtable.update(record['id'], fields)


if __name__ == '__main__':
    main()
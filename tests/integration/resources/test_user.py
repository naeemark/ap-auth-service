"""
    A file to containe all integration tests of
    UserResource
"""

import json


def test_sum(test_client, test_database):
    """
        A sample test to demostrate the availability of test_client and test_dataabase
    """
    # for mock purpose
    # pylint: disable=unused-argument
    assert 1 + 1 == 2


def test_password_change(test_client, test_database):
    content_type_key = 'Content-Type'
    content_type_value = 'application/json'

    response_start_session = test_client.post('/dev/api/v1/user/StartSession',
                                              headers=
                                              {
                                                  'Client-App-Token': '0b0069c752ec14172c5f78208f1863d7ad6755a6fae6fe76ec2c80d13be41e42',
                                                  'Timestamp': '131231',
                                                  'Device-ID': '1321a31x121za'
                                              })

    access_token_session = json.loads(response_start_session.data)['access_token']

    response_register_user = test_client.post('/dev/api/v1/user/register',
                                              headers=
                                              {
                                                  'Authorization': f'Bearer {access_token_session}',
                                                  content_type_key: content_type_value
                                              },

                                              data=json.dumps(
                                                  {
                                                      'email': 'john12@gmail.com',
                                                      'password': '123!!@@AB'
                                                  }
                                              )
                                              )

    access_token_register = json.loads(response_register_user.data)['access_token']

    response_login_user = test_client.post('/dev/api/v1/user/login',
                                           headers=
                                           {
                                               'Authorization': f'Bearer {access_token_register}',
                                               content_type_key: content_type_value
                                           },

                                           data=json.dumps(
                                               {
                                                   'email': 'john12@gmail.com',
                                                   'password': '123!!@@AB'
                                               }
                                           )
                                           )
    fresh_access_token_login = json.loads(response_login_user.data)['fresh_token']

    response_password_change = test_client.put('/dev/api/v1/user/changePassword',
                                               headers=
                                               {
                                                   'Authorization': f'Bearer {fresh_access_token_login}',
                                                   content_type_key: content_type_value
                                               },

                                               data=json.dumps(
                                                   {
                                                       'new_password': '7897!!@@AB'
                                                   }
                                               )
                                               )
    assert response_password_change.status_code == 200

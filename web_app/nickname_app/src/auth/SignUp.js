import UserPool from '../UserPool';
import { CognitoUserAttribute } from 'amazon-cognito-identity-js';
// This is the same user pool we created in the above step

export async function signUp(name, email, password, metaData) {
  const attributeList = [
    new CognitoUserAttribute({
      Name: 'name',
      Value: name,
    }),
    // add other needed attributes here
  ];

  await new Promise((resolve, reject) => {
    UserPool.signUp(
      email,
      password,
      attributeList,
      [],
      (error, result) => {
        if (error) {
          reject(error);
        }

        if (result) {
          resolve(result);
        }
      },
      { ...metaData },
    );
  });
}

export default signUp;
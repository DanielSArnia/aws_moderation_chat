import UserPool from '../UserPool';
import {
    AuthenticationDetails,
    CognitoUser,
} from 'amazon-cognito-identity-js';

export function getUser(email) {
    const userData = {
        Username: email,
        Pool: UserPool, // Make sure UserPool is defined somewhere in your code
    };

    return new CognitoUser(userData);
}

export async function AuthenticateUser(email, password) {
    return new Promise((resolve, reject) => {
        const cognitoUser = getUser(email);

        const authenticationData = {
            Username: email,
            Password: password,
        };
        const authenticationDetails = new AuthenticationDetails(authenticationData);

        cognitoUser.authenticateUser(authenticationDetails, {
            onSuccess: (session, userConfirmationNecessary) => {
                const accessToken = session.getAccessToken().getJwtToken();
                const refreshToken = session.getRefreshToken().getToken();
                resolve({
                    type: 'SUCCESS',
                    session,
                    userConfirmationNecessary,
                    cognitoUser,
                    accessToken,
                    refreshToken,
                });
            },

            onFailure: (err) => reject(err),

            newPasswordRequired: (userAttributes, requiredAttributes) => {
                resolve({
                    type: 'NEW_PASSWORD_REQUIRED',
                    userAttributes,
                    requiredAttributes,
                    cognitoUser,
                });
            },

            totpRequired: (challengeName, challengeParameters) => {
                resolve({
                    type: 'TOTP_REQUIRED',
                    challengeName,
                    challengeParameters,
                    cognitoUser,
                });
            },

            mfaSetup: (challengeName, challengeParameters) => {
                resolve({
                    type: 'MFA_SETUP',
                    challengeName,
                    challengeParameters,
                    cognitoUser,
                });
            },
        });
    });
}

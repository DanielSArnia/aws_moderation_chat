import { getUser } from "./Login";

export async function confirmSignUp(email, code) {
    const cognitoUser = getUser(email);
    await new Promise((resolve, reject) => {
        cognitoUser.confirmRegistration(code, true, (err, result) => {
            if (err) {
                reject(err);
            }
            if (result) {
                resolve(cognitoUser);
            }
        });
    });
}

export function resendCode(email) {
    const cognitoUser = getUser(email);
    cognitoUser.resendConfirmationCode((err, result) => {
        if (err) {
            // Some error message on screen or a toast
            return;
        }
        // Some toast or message displayed on screen of success
    });
}
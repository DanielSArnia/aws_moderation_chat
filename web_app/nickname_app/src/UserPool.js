import { CognitoUserPool } from 'amazon-cognito-identity-js';

// Set up the user pool data using environment variables
const poolData = {
  UserPoolId: import.meta.env.VITE_USER_POOL_ID,
  ClientId: import.meta.env.VITE_USER_POOL_CLIENT_ID,
};

export default new CognitoUserPool(poolData);
const API_VERSION = 'v1';

export const user_api_base = (userId: string | number | undefined) => {
  return userId ? `/api/${API_VERSION}/users/${userId}` : '/api/v1/users';
};


export const bot_api_base = (botId: string | number | undefined) => {
    return botId ? `/api/${API_VERSION}/bots/${botId}` : '/api/v1/bots';
  };
  
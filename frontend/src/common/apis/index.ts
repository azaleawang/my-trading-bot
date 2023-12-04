export const user_api_base = (userId: string | number | undefined) => {
  return userId ? `/api/v1/users/${userId}` : '/api/v1/users';
};


export const bot_api_base = (botId: string | number | undefined) => {
    return botId ? `/api/v1/bots/${botId}` : '/api/v1/bots';
  };
  
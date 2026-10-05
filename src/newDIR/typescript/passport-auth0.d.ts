declare module 'passport-auth0' {
  export class Strategy {
    constructor(
      options: { domain: string; clientID: string; clientSecret: string; callbackURL: string },
      verify: (
        accessToken: string,
        refreshToken: string,
        extraParams: unknown,
        profile: unknown,
        done: (err: Error | null, user?: unknown) => void
      ) => void
    );
  }
}

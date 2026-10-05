import passport from 'passport';
import { Strategy as JwtStrategy } from 'passport-jwt';
import { Strategy as Auth0Strategy } from 'passport-auth0';
import jsonwebtoken from 'jsonwebtoken';
import type { JwtPayload } from '../types';

const jwtOptions = {
  jwtFromRequest: (req: { headers: { authorization?: string } }) => {
    const auth = req.headers.authorization;
    return auth?.startsWith('Bearer ') ? auth.slice(7) : null;
  },
  secretOrKey: process.env.JWT_SECRET ?? 'dev-secret',
};

passport.use(
  new JwtStrategy(jwtOptions, (payload: JwtPayload, done) => {
    done(null, { id: payload.sub, email: payload.email });
  })
);

if (process.env.AUTH0_DOMAIN && process.env.AUTH0_CLIENT_ID) {
  const auth0Strategy = new Auth0Strategy(
    {
      domain: process.env.AUTH0_DOMAIN,
      clientID: process.env.AUTH0_CLIENT_ID,
      clientSecret: process.env.AUTH0_CLIENT_SECRET ?? '',
      callbackURL: process.env.AUTH0_CALLBACK_URL ?? '/auth/callback',
    },
    (_accessToken: unknown, _refreshToken: unknown, _extraParams: unknown, profile: unknown, done: (err: Error | null, user?: unknown) => void) => {
      done(null, profile);
    }
  );
  passport.use(auth0Strategy as passport.Strategy);
}

export function signToken(payload: JwtPayload): string {
  return jsonwebtoken.sign(payload, process.env.JWT_SECRET ?? 'dev-secret', {
    expiresIn: '7d',
  });
}

export const jwtAuth = passport.authenticate('jwt', { session: false });

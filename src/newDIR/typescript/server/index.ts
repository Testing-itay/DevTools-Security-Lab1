import * as Sentry from '@sentry/node';
import winston from 'winston';
import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import passport from 'passport';
import { createServer } from 'http';
import { initTelemetry } from '../observability/telemetry';
import { connectMongo } from '../data/mongo-repository';
import { registerRoutes } from './routes';
import { initSocketHandler } from '../realtime/socket-handler';

Sentry.init({
  dsn: process.env.SENTRY_DSN,
  environment: process.env.NODE_ENV ?? 'development',
});

initTelemetry();

const app = express();
app.use(Sentry.Handlers.requestHandler());
app.use(helmet());
app.use(cors({ origin: process.env.CORS_ORIGIN ?? '*' }));
app.use(express.json());
app.use(passport.initialize());

registerRoutes(app);

app.use(Sentry.Handlers.errorHandler());

const httpServer = createServer(app);
initSocketHandler(httpServer);

const port = Number(process.env.PORT) || 3000;

const logger = winston.createLogger({
  level: 'info',
  format: winston.format.json(),
  transports: [new winston.transports.Console()],
});

connectMongo(process.env.MONGO_URI ?? 'mongodb://localhost:27017/devtools')
  .then(() => {
    httpServer.listen(port, () => {
      logger.info(`Server listening on port ${port}`);
    });
  })
  .catch((err) => {
    logger.error('Failed to connect to MongoDB', { error: err });
    process.exit(1);
  });

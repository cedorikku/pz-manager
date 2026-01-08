import cors from 'cors';
import express from 'express';

import indexRouter from './routes/indexRouter.js';

const app = express();

app.use(cors());
app.use(express.json());
app.use(express.urlencoded());

app.use('/', indexRouter);

export default app;

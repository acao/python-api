import Koa from "koa";
import convert from "koa-convert";
import PythonShell from "python-shell";
import body from "koa-better-body";

import logger, { koaLogger } from "./logger";
import config from "./config.json";

const app = new Koa();
const router = require('koa-router')({ prefix: "/calculate" });
const port = process.env.PORT || 9003;

app.use(convert(koaLogger));

async function runScript(data, script) {
  return new Promise((res, rej)=>{
    PythonShell.run(`python/${script.path}`, {mode: 'text', args: [JSON.stringify(data)]}, (e, results) => {
      if (e) rej(e);
      else {
        res(JSON.parse(results));
      }
    });
  });
}

for (var i = 0; i < config.scripts.length; i++) {
  const script = config.scripts[i];
  router.post(`/${script.name}`, async(ctx, next) => {
    try {
      ctx.body = await runScript(ctx.body, script);
      ctx.status = 200;
      logger.info(`${script.name} script executed successfully`);
      await next(); // next is now a function
    } catch (err) {
      ctx.body = { message: err.message };
      ctx.status = err.status || 500;
      logger.error(`${script.name} script failed with ${err.message}`)
      await next(); // next is now a function
    }
  });
}


app
  .use(router.routes())
  .use(router.allowedMethods());

app.listen(port);
logger.info(`now listening on http://localhost:${port}`);

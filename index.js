import fs from "fs";
import Koa from "koa";
import convert from "koa-convert";
import PythonShell from "python-shell";
import body from "koa-better-body";
import toml from "toml";

import logger, { koaLogger } from "./logger";

const config = toml.parse(fs.readFileSync("./config.toml"));

const router = require('koa-router')({ prefix: "/calculate" });
const app = new Koa();
const port = process.env.PORT || 9003;
const { scripts } = config;

app.use(convert(body()));
app.use(convert(koaLogger));

async function runScript(script, data) {
  return new Promise((res, rej)=> {
    const postData = script.singleArg ? [JSON.stringify(data)] : [data.map((item) => JSON.stringify(data))];
    PythonShell.run(`python/${script.path}`, {args: postData}, (e, results) => {
       if (e) rej(e);
       else {
          res(JSON.parse(results));
       }
    });
  });
}

for (var i = 0; i < scripts.length; i++) {
  const script = scripts[i];
  router.post(`/${script.name}`, async(ctx, next) => {
    try {
      ctx.body = await runScript(script, ctx.body);
      ctx.status = 200;
      logger.info(`${script.name} script executed successfully`);
      await next();
    } catch (err) {
      ctx.body = { message: err.message };
      ctx.status = err.status || 500;
      logger.error(`${script.name} script failed with ${err.message}`)
      await next();
    }
  });
}


app
  .use(router.routes())
  .use(router.allowedMethods());

app.listen(port);
logger.info(`now listening on http://localhost:${port}`);

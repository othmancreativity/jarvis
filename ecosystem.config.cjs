const fs = require("fs");
const path = require("path");

const root = __dirname;
let logsDir = path.join(root, "logs");
try {
  const raw = fs.readFileSync(path.join(root, "paths.json"), "utf8");
  const p = JSON.parse(raw);
  if (p.dirs && typeof p.dirs.logs === "string") {
    logsDir = path.isAbsolute(p.dirs.logs) ? p.dirs.logs : path.join(root, p.dirs.logs);
  }
} catch (_) {
  /* defaults */
}

module.exports = {
  apps: [
    {
      name: "jarvis",
      script: "dist/index.js",
      node_args: "--experimental-vm-modules",
      cwd: __dirname,
      watch: false,
      autorestart: true,
      max_restarts: 50,
      restart_delay: 5000,
      env: {
        NODE_ENV: "production",
      },
      error_file: path.join(logsDir, "error.log"),
      out_file: path.join(logsDir, "out.log"),
      merge_logs: true,
      log_date_format: "YYYY-MM-DD HH:mm:ss",
    },
  ],
};

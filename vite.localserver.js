import { resolve } from "node:path";
import { existsSync, statSync, readFileSync, readdirSync } from "node:fs";

/**
 * Creates a Vite plugin to serve the databases_served folder during development (local)
 * @param {string} __dirname - The directory name of the main config file
 * @returns {object|null} Vite plugin object or null if not in serve mode
 */
export function createDatabasesServedServer(__dirname) {
  return {
    name: "serve-databases-served",
    configureServer(server) {
      server.middlewares.use((req, res, next) => {
        if (req.url && req.url.startsWith("/dea/dea_db")) {
          console.log(`Intercepted request: ${req.url}`);
          
          // Remove the /dea/served prefix
          let requestPath = req.url.replace("/dea/dea_db", "");

          // Remove query parameters if any
          const queryIndex = requestPath.indexOf('?');
          if (queryIndex !== -1) {
            requestPath = requestPath.substring(0, queryIndex);
          }
          
          // If requesting the root of served, show directory listing
          if (requestPath === "" || requestPath === "/") {
            requestPath = "";
          } else {
            // Remove leading slash
            requestPath = requestPath.startsWith('/') ? requestPath.slice(1) : requestPath;
          }
          
          const filePath = requestPath ? resolve(__dirname, "..", "dea_db", requestPath) : resolve(__dirname, "databases_management", "databases_served");
          
          console.log(`Serving databases_served request: ${req.url} -> ${filePath}`);
          
          try {
            console.log(`Checking if path exists: ${filePath}`);
            if (existsSync(filePath)) {
              const stat = statSync(filePath);
              console.log(`Path exists. Is file: ${stat.isFile()}, Is directory: ${stat.isDirectory()}`);
              if (stat.isFile()) {
                const content = readFileSync(filePath);
                console.log(`File content length: ${content.length}`);
                
                // Set appropriate content type based on file extension
                if (filePath.endsWith('.py')) {
                  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
                } else if (filePath.endsWith('.json')) {
                  res.setHeader('Content-Type', 'application/json; charset=utf-8');
                } else if (filePath.endsWith('.html')) {
                  res.setHeader('Content-Type', 'text/html; charset=utf-8');
                } else if (filePath.endsWith('.png')) {
                  res.setHeader('Content-Type', 'image/png');
                } else if (filePath.endsWith('.jpg') || filePath.endsWith('.jpeg')) {
                  res.setHeader('Content-Type', 'image/jpeg');
                } else if (filePath.endsWith('.gif')) {
                  res.setHeader('Content-Type', 'image/gif');
                } else if (filePath.endsWith('.svg')) {
                  res.setHeader('Content-Type', 'image/svg+xml');
                } else if (filePath.endsWith('.webp')) {
                  res.setHeader('Content-Type', 'image/webp');
                } else if (filePath.endsWith('.ico')) {
                  res.setHeader('Content-Type', 'image/x-icon');
                } else if (filePath.endsWith('.pdf')) {
                  res.setHeader('Content-Type', 'application/pdf');
                } else if (filePath.endsWith('.txt')) {
                  res.setHeader('Content-Type', 'text/plain; charset=utf-8');
                } else if (filePath.endsWith('.css')) {
                  res.setHeader('Content-Type', 'text/css; charset=utf-8');
                } else if (filePath.endsWith('.js')) {
                  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
                } else {
                  res.setHeader('Content-Type', 'application/octet-stream');
                }
                res.end(content);
                return;
              } else if (stat.isDirectory()) {
                // List directory contents
                const files = readdirSync(filePath);
                console.log(`Directory contains ${files.length} files: ${files.join(', ')}`);
                const displayPath = req.url.replace("/dea/served", "") || "/";
                const html = `
                  <html>
                    <head><title>Directory: ${displayPath}</title></head>
                    <body>
                      <h2>Directory listing for ${displayPath}</h2>
                      <ul>
                        ${displayPath !== "/" ? `<li><a href="../">../</a></li>` : ""}
                        ${files.map(file => {
                          const href = `/dea/served${displayPath === "/" ? "" : displayPath}/${file}`;
                          return `<li><a href="${href}">${file}</a></li>`;
                        }).join('')}
                      </ul>
                    </body>
                  </html>
                `;
                console.log(`Sending directory listing HTML (${html.length} characters)`);
                res.setHeader('Content-Type', 'text/html; charset=utf-8');
                res.end(html);
                return;
              }
            } else {
              console.log(`File not found: ${filePath}`);
            }
          } catch (error) {
            console.error('Error serving databases_management:', error);
          }
          res.statusCode = 404;
          res.end('Not found');
          return;
        }
        next();
      });
    }
  };
}

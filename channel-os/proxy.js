// Minimal CORS proxy — forwards browser requests to Anthropic API
import http from 'http';
import https from 'https';

const PORT = process.env.PORT || 3001;

const CORS_HEADERS = {
  'Access-Control-Allow-Origin': '*',
  'Access-Control-Allow-Methods': 'POST, OPTIONS',
  'Access-Control-Allow-Headers': 'Content-Type, x-api-key, anthropic-version',
};

http.createServer((req, res) => {
  // CORS preflight
  if (req.method === 'OPTIONS') {
    res.writeHead(204, CORS_HEADERS);
    res.end();
    return;
  }

  if (req.method === 'POST' && req.url === '/api/claude') {
    let body = '';
    req.on('data', chunk => (body += chunk));
    req.on('end', () => {
      const apiKey = req.headers['x-api-key'];
      const anthropicVersion = req.headers['anthropic-version'] || '2023-06-01';
      const bodyBuffer = Buffer.from(body);

      const proxyReq = https.request(
        {
          hostname: 'api.anthropic.com',
          path: '/v1/messages',
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Content-Length': bodyBuffer.length,
            'x-api-key': apiKey,
            'anthropic-version': anthropicVersion,
          },
        },
        proxyRes => {
          res.writeHead(proxyRes.statusCode, {
            'Content-Type': 'application/json',
            ...CORS_HEADERS,
          });
          proxyRes.pipe(res);
        }
      );

      proxyReq.on('error', err => {
        res.writeHead(502, { 'Content-Type': 'application/json', ...CORS_HEADERS });
        res.end(JSON.stringify({ error: { message: err.message } }));
      });

      proxyReq.write(bodyBuffer);
      proxyReq.end();
    });
    return;
  }

  // Health check
  if (req.url === '/health') {
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('ok');
    return;
  }

  res.writeHead(404);
  res.end('Not found');
}).listen(PORT, () => console.log(`channel-os-proxy running on port ${PORT}`));

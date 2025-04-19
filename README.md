# ThreatLog-AI-API

<hr>

<h3>Prerequisites</h3>
<p>Before running the application, ensure that you have the following installed:</p>

<ul>
	<li><b>Python 3.12</b> - Ensure you have Python version 3.12 installed.</li>
  <li><b>SQL Database</b> - MySQL or MariaDB is required to store application data.</li>
</ul>

<h3>Setup</h3>
<pre>
<code>git clone https://github.com/DeathLockers/ThreatLog-AI-API.git</code>
</pre>
<pre>
<code>cd ThreatLog-AI-API</code>
</pre>
<pre>
<code>cp .env.example .env</code>
</pre>
<pre>
<code>pip install --no-cache-dir --upgrade -r requirements.txt</code>
</pre>
<pre>
<code>fastapi run app/main.py --port 8000 --reload</code>
</pre>
<pre>
<code>sed -i '/JWT_SECRET_KEY=""/d' .env && jwt_secret_key="JWT_SECRET_KEY=$(openssl rand -hex 32)" && sed -i -e "11i$jwt_secret_key" .env</code>
</pre>
<pre>
<code>python -m app.db.migration</code>
</pre>

<hr>

<h3>API documentation summary</h3>
<p></p>
<span>User: <b>client1@email.com</b></span><br>
<span>Password: <b>Pass-1234</b></span>

<h4>Headers</h4>
<table>
<thead>
<tr>
<th>Key</th>
<th>Value</th>
</tr>
</thead>
<tbody>
<tr>
<td>Authorization</td>
<td>{Token provided by JWT}</td>
</tr>
<tr>
<td>Accept</td>
<td>application/json</td>
</tr>
</tbody>
</table>

<h4>Endpoints Auth:</h4>
<table>
<thead>
<tr>
<th>Method</th>
<th>Path</th>
<th>Description</th>
<th>Auth</th>
</tr>
</thead>
<tbody>
<tr>
<td>POST</td>
<td>/auth/login</td>
<td>Login a user</td>
<td>No</td>
</tr>
<tr>
<td>GET</td>
<td>/auth/me</td>
<td>Check if user authenticated</td>
<td>Yes</td>
</tr>
</tbody>
</table>

<h4>Endpoints Logs:</h4>
<table>
<thead>
<tr>
<th>Method</th>
<th>Path</th>
<th>Description</th>
<th>Auth</th>
</tr>
</thead>
<tbody>
<tr>
<td>POST</td>
<td>/logs</td>
<td>Show logs</td>
<td>Yes</td>
</tr>
<tr>
<td>GET</td>
<td>/logs/charts/line_periods<br>/logs/charts/log_total_types<br>/logs/charts/log_count_types_period</td>
<td>Returns log statistics to be displayed in a visual graph</td>
<td>Yes</td>
</tr>
<tr>
<td>POST</td>
<td>/verified_logs/</td>
<td>So that the user can verify logs if it is a false positive or not.</td>
<td>Yes</td>
</tr>
</tbody>
</table>

<span> More information API documentation: <a href="http://localhost:8000/docs" target="_blank">http://localhost:8000/docs</a>
</span>

<hr>



<h3>Configure values in the .env file</h3>

<pre><code><strong>DB_DRIVER=""</strong>
<strong>DB_HOST=""</strong>
<strong>DB_PORT=""</strong>
<strong>DB_DATABASE=""</strong>
<strong>DB_USERNAME=""</strong>
<strong>DB_PASSWORD=""</strong>
</code></pre>

<pre><code><span># command generate JWT_SECRET_KEY: openssl rand -hex 32</span>
<strong>JWT_SECRET_KEY=""</strong>
<strong>JWT_ALGORITHM="HS256"</strong>
</code></pre>

<pre><code><strong>TIMEZONE=""</strong>
</code></pre>

<pre><code><span># CORS</span>
<strong>DOMAINS_ORIGINS_LIST="http://localhost:9000,http://127.0.0.1:9000"</strong>
</code></pre>

<pre><code><span># KAFKA</span>
<strong>KAFKA_HOST=""</strong>
<strong>KAFKA_CONSUMER_TOPIC=""</strong>
</code></pre>

<hr>

<h3>Deploy to Docker <g-emoji class="g-emoji" alias="whale" fallback-src="https://github.githubassets.com/images/icons/emoji/unicode/1f433.png">🐳</g-emoji></h3>

<h4>Containers:</h4>
<ul>
<li><span>python:3.12</span> - <code>:8000</code></li>
<li><span>mariadb:11.6.2</span> - <code>:3306</code></li>
</ul>

<h4>Containers structure:</h4>
<div class="highlight highlight-source-shell"><pre>├── threatlog-ai-api
└── threatlog-ai-db</pre></div>

<h4>Setup:</h4>
<pre>
<code>git clone https://github.com/DeathLockers/ThreatLog-AI-API.git</pre></code>
<pre><code>cd ThreatLog-AI-API</pre></code>
<pre><code>cp .env.example .env</pre></code>
<pre><code>docker compose up -d</pre></code>
<pre><code>docker compose exec app chmod +x ./docker-config/run.sh</pre></code>
<pre><code>docker compose exec app ./docker-config/run.sh</code>
</pre>

<span>Once you have the containers deployed, you can access the API at </span> <a href="http://localhost:8000" target="_blank">http://localhost:8000</a>

<hr>

<h4>It also includes:</h4>
<ul>
<li><a href="https://github.com/DeathLockers/ThreatLog-AI-API/ThreatLog%20API.postman_collection.json"  target="_blank">ThreatLog API.postman_collection.json</a> file for importing and testing the API REST.</li>

<li><a href="https://github.com/DeathLockers/ThreatLog-AI-API/threatlog_ai_api.sql"  target="_blank">threatlog_ai_api.sql</a> file for importing data for the various database tables.</li>
</ul>
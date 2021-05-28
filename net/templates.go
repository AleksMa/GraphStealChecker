package net

var StartTemplate = `
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>/api/tarantool/</title>
</head>
<style type="text/css">
	* {
		font-family: "Helvetica", sans-serif;
		margin: 0;
		padding: 0;
	}

	.container {
		display: flex;
	}

	.left, .right {
		min-width: 30%;
		word-break: break-all;
		flex-grow: 1;
	}

	.base_block {
		margin-top: 10px;
	}

	.error {
		color: #dc143c;
		margin-top: 10px;
	}

	.response {
		font-family: "Fira Mono", monospace;
		font-size: 12px;
		border: 1px solid;
		border-radius: 5px;
		padding: 10px;
		display: inline-block;
	}

	.mb {
		margin-bottom: 5px;
	}

	body {
		margin: 10px;
	}

	h3 {
		margin-bottom: 5px;
	}

	h5 {
		margin-bottom: 5px;
	}
</style>
<body>
<h3>Input</h3>
<form action="/check" method="POST" enctype="multipart/form-data">
	<div class="mb">
		<input type="file" id="p1" name="p1">
		<input type="file" id="p2" name="p2">
	</div>
	<div>
		Time limit:
		<input type="text" id="limit" name="limit" value="5">
	</div>
	<div>
		Subgraph size:
		<input type="text" id="subgraph" name="subgraph" value="0.7">
	</div>
	<div>
		Likelihood:
		<input type="text" id="likelihood" name="likelihood" value="0.9">
	</div>
	<div>
		<input type="submit" value="Проверить!"/>
	</div>
</form>
</body>
</html>`

var CheckTemplate = `<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="UTF-8">
	<title>/api/tarantool/</title>
</head>
<style type="text/css">
	* {
		font-family: "Helvetica", sans-serif;
		margin: 0;
		padding: 0;
	}

	.container {
		display: flex;
	}

	.left, .right {
		min-width: 30%;
		word-break: break-all;
		flex-grow: 1;
	}

	.base_block {
		margin-top: 10px;
	}

	.error {
		color: #dc143c;
		margin-top: 10px;
	}

	.response {
		font-family: "Fira Mono", monospace;
		font-size: 12px;
		border: 1px solid;
		border-radius: 5px;
		padding: 10px;
		display: inline-block;
	}

	.mb {
		margin-bottom: 5px;
	}

	body {
		margin: 10px;
	}

	h3 {
		margin-bottom: 5px;
	}

	h5 {
		margin-bottom: 5px;
	}
</style>
<body>
<h3>Plagiarism</h3>
		<div class="container">
			<div class="left">
				<div class="response">
				{{range .FileLeft}}
					<p style="color:{{.Color}};">
						{{.Line}}
					</p>
				{{end}}
				</div>
			</div>
			<div class="right">
				<div class="response">
				{{range .FileRight}}
					<p style="color:{{.Color}};">
						{{.Line}}
					</p>
				{{end}}
				</div>
			</div>
		</div>
</body>
`

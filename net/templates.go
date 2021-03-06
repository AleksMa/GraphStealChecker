package net

// HTML-разметка страниц ввода данных и отображения результатов

var StartTemplate = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ввод</title>

</head>
<style type="text/css">
    * {
        font-family: "Helvetica", sans-serif;
        margin: 0;
        padding: 0;
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

    .field__wrapper {
        position: relative;
        margin: 15px 0;
        text-align: center;
    }

    .field__file {
        opacity: 0;
        visibility: hidden;
        position: absolute;
    }

    .field__file-wrapper {
        width: 100%;
        display: -webkit-box;
        display: -ms-flexbox;
        display: flex;
        -webkit-box-align: center;
        -ms-flex-align: center;
        align-items: center;
        -ms-flex-wrap: wrap;
        flex-wrap: wrap;
    }

    .field__file-fake {
        padding: 5px 15px;
        border: 1px solid #c7c7c7;
    }

    .field__file-button {
        background: #1bbc9b;
        color: #fff;
        padding: 5px 5px;
        border: 1px solid #c7c7c7;
    }
</style>

<body>

<h3>Ввод</h3>
<form action="/check" method="POST" enctype="multipart/form-data">

    <div class="field__wrapper">
        <input name="p1" type="file" id="p1" class="field field__file" accept=".py">
        <label class="field__file-wrapper" for="p1">
            <div class="field__file-fake">Файл не выбран</div>
            <div class="field__file-button">Выбрать</div>
        </label>
        <input name="p2" type="file" id="p2" class="field field__file" accept=".py">
        <label class="field__file-wrapper" for="p2">
            <div class="field__file-fake">Файл не выбран</div>
            <div class="field__file-button">Выбрать</div>
        </label>
    </div>

    <table>
        <tr>
            <td>
                Лимит времени проверки:
            </td>
            <td>
                <input type="text" id="limit" name="limit" value="20">
            </td>
        </tr>
        <tr>
            <td>
                Минимальная доля вершин при сравнении:
            </td>
            <td>
                <input type="text" id="subgraph" name="subgraph" value="0.9">
            </td>
        </tr>
        <tr>
            <td>
                Уровень правдоподобия:
            </td>
            <td>
                <input type="text" id="likelihood" name="likelihood" value="0.99">
            </td>
        </tr>
    </table>
    <div>
        <input type="submit" value="Проверить!"/>
    </div>
</form>


<script>
    let fields = document.querySelectorAll('.field__file');
    Array.prototype.forEach.call(fields, function (input) {
        let label = input.nextElementSibling,
            labelVal = label.querySelector('.field__file-fake').innerText;

        input.addEventListener('change', function (e) {
            let countFiles = '';
            if (this.files && this.files.length >= 1)
                countFiles = this.files.length;

            if (countFiles)
                label.querySelector('.field__file-fake').innerText = this.files[0].name;
            else
                label.querySelector('.field__file-fake').innerText = labelVal;
        });
    });
</script>

</body>
</html>`

var CheckTemplate = `
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Результат</title>
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

    .response {
        font-family: "Fira Mono", monospace;
        font-size: 12px;
        border: 1px solid;
        border-radius: 5px;
        padding: 10px;
        display: inline-block;
    }

    .code_text {
        font-family: "Fira Mono", monospace;
        font-size: 14px;
    }

    .mb {
        margin-top: 5px;
        margin-bottom: 10px;
    }

    .mr {
        padding-right: 30px;
    }

    body {
        margin: 10px;
    }

    h2 {
        margin-top: 5px;
        margin-bottom: 10px;
    }

    h3 {
        margin-top: 5px;
        margin-bottom: 10px;
    }

    h5 {
        margin-bottom: 5px;
    }
</style>
<body>
<h2>Результат сравнения</h2>
<div class="mb">
    Общая доля заимствований: {{ .Plagiarism }}%
</div>
<div class="mb">
    <h3> Заимствования по функциям: </h3>
    <table>
        {{range .PlagFuncs}}
            <tr>
                <td class="mr code_text">
                    {{ .FuncLeft }}
                </td>
                <td class="mr code_text">
                    {{ .FuncRight }}
                </td>
                <td>
                    {{ .Plagiarism }}%
                </td>
            </tr>
        {{end}}
    </table>

    <h3> Заимствования в исходном тексте: </h3>
</div>
<div class="container">
    <div class="left">
        <h5>{{ .NameLeft }} </h5>
        <div class="response">
            {{range .LinesLeft}}
                {{ if .Parsed }}
                    <p style="color:{{.Color}};">
                        {{.Line}}
                    </p>
                {{ end }}
            {{end}}
        </div>
    </div>
    <div class="right">
        <h5>{{ .NameRight }} </h5>
        <div class="response">
            {{range .LinesRight}}
                {{ if .Parsed }}
                    <p style="color:{{.Color}};">
                        {{.Line}}
                    </p>
                {{ end }}
            {{end}}
        </div>
    </div>
</div>

</body>
`

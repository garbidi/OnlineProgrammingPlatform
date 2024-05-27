const output = document.getElementById("output");

const editor = CodeMirror.fromTextArea(document.getElementById("code"), {
	mode: {
		name: "python",
		version: 3,
		singleLineStringErrors: false
	},
	lineNumbers: true,
	indentUnit: 4,
	matchBrackets: true
});

editor.setValue(`print("Hello, World!")`);
output.value = "Initializing...\n";

async function main() {
	let pyodide = await loadPyodide({ indexURL: "https://cdn.jsdelivr.net/pyodide/v0.18.1/full/" });
	// Pyodide ready
	output.value += "Ready!\n";
	return pyodide;
};

let pyodideReadyPromise = main();

function addToOutput(s) {
	output.value += ">>>" + s + "\n";
}

async function evaluatePython() {
  let pyodide = await pyodideReadyPromise;
  try {
    let output = '';
    pyodide.runPython(`
import sys
from io import StringIO

sys.stdout = StringIO()
try:
    exec('''${editor.getValue()}''')
    output = sys.stdout.getvalue()
except Exception as e:
    output = str(e)
sys.stdout = sys.__stdout__

print(output)
`);
    output = pyodide.runPython('output');
    addToOutput(output);
  } catch (err) {
    addToOutput(err);
  }
}


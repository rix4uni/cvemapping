import soot.*;
import soot.options.Options;
import java.util.Collections;

public class POC {
    public static void main(String[] args) {
        // Initialize Soot
        G.reset();

        // Set Soot options
        Options.v().set_prepend_classpath(true); // Use the standard classpath
        Options.v().set_src_prec(Options.src_prec_class); // Process only .class files
        Options.v().set_output_dir("jimple_output"); // Directory to store Jimple output
        Options.v().set_output_format(Options.output_format_jimple); // Set output format to Jimple
        Options.v().set_process_dir(Collections.singletonList("src/main/resources")); // Path to payload
        Options.v().set_allow_phantom_refs(true);

        // Load classes and finish initialization
        Scene.v().loadNecessaryClasses();

        SootClass sootClass = Scene.v().getSootClass("Build$Builder"); // Build$Builder Class file as payload
        for (SootMethod method : sootClass.getMethods()) {
            System.out.println(method.getSignature());
            method.retrieveActiveBody(); // It will get stuck at <Build$Builder: org.apache.maven.api.model.Build build()>
        }

    }

}
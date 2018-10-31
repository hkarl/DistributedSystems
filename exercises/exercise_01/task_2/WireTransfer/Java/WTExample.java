import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.net.ServerSocket;
import java.net.Socket;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;

//Flatbuffers java library package
//Downloaded from GitHub
import com.google.flatbuffers.FlatBufferBuilder;
//Package for wire transfer structure
//Generated with flatc compiler
import VS.wire_transfer.*;


public class WTExample {
	
	public static void main(String[] args) {
		
		Socket sockToC = null;
		try {
			ServerSocket ss = new ServerSocket(9999);
			sockToC = ss.accept();
			ss.close();
			
			System.out.println("Connection established");
			InputStream in = sockToC.getInputStream();
			OutputStream out = sockToC.getOutputStream();
			
			// Start flatbuffer object construction
			// Create builder object
			FlatBufferBuilder builder = new FlatBufferBuilder(0);
			
			// Create data for Message
			String string_message = "Greetings from the Java world.";
			int byteVec_message = builder.createByteVector(string_message.getBytes(StandardCharsets.US_ASCII));
			int from = builder.createString("Java");
            //Create MessageHeader
			int head = MessageHeader.createMessageHeader(builder, Type.PUSH, 28);
			
			// Create Message
			Message.startMessage(builder);
			Message.addHeader(builder, head);
			Message.addFrom(builder, from);
			Message.addHasContent(builder, true);
			Message.addContent(builder, byteVec_message);
			int m = Message.endMessage(builder);
			
			// End flatbuffer object construction
			builder.finish(m);
			
			// Send serialized data over network
			byte[] serialized_message = builder.sizedByteArray();
			out.write(serialized_message);
			System.out.println("Send bytes: " + serialized_message.length);
			
		    
			// Receive serialized data over network
		   byte[] rbuffer = new byte[1024];
		   int size = 0;
		   size = in.read(rbuffer);
         sockToC.close();

		   ByteBuffer rbuf = ByteBuffer.wrap(rbuffer);
		   System.out.println("Received bytes: " + size);
		    
		   // Access structured data
		   Message response = Message.getRootAsMessage(rbuf);
		   MessageHeader mHeader = response.header();
		    
		   System.out.println("request: " + Type.name(mHeader.request()));
		   System.out.println("seq_num: " + mHeader.seqNum());
		    
		   System.out.println("from: " + response.from());
		   System.out.println("hasContent: " + response.hasContent());
		   System.out.println("content length: " + response.contentLength());

         // Interpret byte as char for the sake of this example
		   for(int i=0; i<response.contentLength(); i++) {
		    	System.out.print((char)response.content(i));
		   }
		   System.out.println("");
			
		} catch (IOException e) {
			e.printStackTrace();
		}		
	}
}

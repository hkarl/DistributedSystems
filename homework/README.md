
# FlatBuffers example

## What it is
This example shows you, how to utilize FlatBuffers serialization library to exchange data across different languages. See [FlatBuffers](https://google.github.io/flatbuffers/) and [FlatCC](https://github.com/dvidelabs/flatcc) for more information.

## Interface Definition Language (IDL)
FlatBuffers use a IDL called schema language to describe structured data. The file `message.fbs` is a schema, which has to be compiled to the target language.

Use the [flatc](https://google.github.io/flatbuffers/flatbuffers_guide_building.html) compiler to generate Java code:
`flatc --java message.fbs`

The C language binding exists in a separate project named [FlatCC](https://github.com/dvidelabs/flatcc). So you have to use the [flatcc](https://github.com/dvidelabs/flatcc#building) compiler to generate C code:
`flatcc -a message.fsb`

## Use FlatBuffers

### Java
Beside the generated `.java` files you have to include FlatBuffers Java library found [here](https://github.com/google/flatbuffers/tree/master/java/com/google/flatbuffers).


### C
For this example you have to include these generated header files: `message_C_builder.h`, `message_C_reader.h`,  `flatbuffers_common_builder.h`, `flatbuffers_common_reader.h` in the compilation process.

Besides that you need serveral files from the [FlatCC build](https://github.com/dvidelabs/flatcc#building):
* Include headers from `flatcc-0.5.2/include/`
* Link with library `flatcc-0.5.2/lib/libflatccrt.a`, the runtime library is needed for building messages.

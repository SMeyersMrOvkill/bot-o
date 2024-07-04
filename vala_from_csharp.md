# Vala for C# Programmers

This guide describes the syntax differences between Vala and C#, intended as a quick introduction to Vala for programmers who already know C#.

## Source Files and Compilation

- C# files use the `.cs` extension, while Vala files use `.vala` [[6]](https://poe.com/citation?message_id=211460081876&citation=6).
- C# is compiled to CIL (Common Intermediate Language) for .NET/Mono, while Vala is compiled to native code via C as an intermediate step [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

Vala compilation example:
```bash
$ valac source1.vala source2.vala -o program
```

## Using Packages

In Vala, you use the `--pkg` option to include packages:
```bash
$ valac source.vala --pkg gtk+-2.0 -o program
```

## Naming Conventions

Vala uses slightly different naming conventions compared to C# [[6]](https://poe.com/citation?message_id=211460081876&citation=6):

- Classes, structs, delegate types: CamelCase (same as C#)
- Methods, properties, signals: lower_case (different from C#)
- Local variables, fields: lower_case (sometimes different from C#)
- Constants, enum values: UPPER_CASE (different from C#)

## Main Entry Point

In C#, the `Main` method must be inside a class. In Vala, the `main` function can be outside a class [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## System Namespace

C#'s most important namespace is `System`, which is not imported by default. Vala's most important namespace is `GLib`, which is implicitly imported by default [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Value Types

Vala has some differences in value types compared to C# [[6]](https://poe.com/citation?message_id=211460081876&citation=6):
- Sizes of standard types are architecture-dependent
- Additional types: `int8`, `int16`, `int32`, `int64`, `uint8`, `uint16`, `uint32`, `uint64`
- No `byte` or `sbyte` (use `uint8` and `int8` instead)
- No `decimal` type
- `char` in Vala is different from C#'s `char`

## Verbatim String Literals

C# uses `@"verbatim string"`, while Vala uses `"""verbatim string"""` [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Documentation Comments

Vala uses Valadoc comments, which are similar to C# XML comments but with a different syntax [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Object Base Class

In C#, classes implicitly inherit from `object` (System.Object). In Vala, there's no implicit inheritance from `Object` (GLib.Object) [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Method Overloading

Vala doesn't support method overloading. Instead, use different method names or default argument values [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Multiple Constructors

Vala uses named constructors instead of constructor overloading [[6]](https://poe.com/citation?message_id=211460081876&citation=6):

```vala
class Foo : Object {
    public Foo () { }
    public Foo.with_foo (int foo) { }
    public Foo.from_bar (string bar) { }
}
```

## Delegates and Lambdas

Vala supports lambda expressions and direct method assignment for delegates, similar to C# [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Events and Signals

Vala uses signals instead of events. The syntax is slightly different, using `connect` and `disconnect` instead of `+=` and `-=` [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Interfaces

Vala interfaces require the `public abstract` modifier for methods. Interfaces in Vala can have non-abstract methods, allowing them to be used as mixins [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Enums

Vala enums can have methods, which is not directly possible in C# [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Struct Initialization

Vala structs are instantiated without using the `new` operator [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Nullable Types

In Vala, the `?` modifier is used to mark nullable reference type arguments and return values, which are non-nullable by default [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Properties

Vala supports default values for auto-implemented properties and has built-in support for property change notifications [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Exceptions

Vala uses checked exceptions (called "errors") which are not class-based. Error handling in Vala is more explicit than in C# [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Memory Management

While C# uses garbage collection, Vala uses automatic reference counting. This can lead to some differences in handling object lifecycles [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

## Asynchronous Calls

Vala has built-in support for asynchronous methods using the `async` and `yield` keywords [[6]](https://poe.com/citation?message_id=211460081876&citation=6).

This guide covers the main differences between C# and Vala. For more detailed information on specific topics, refer to the full Vala documentation.

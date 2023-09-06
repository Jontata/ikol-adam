### Dev notes:
Make sure that the Flutter SDK is up to date:
```
flutter upgrade
```

For projects with Firestore integration, you must first run the following commands to ensure the project compiles:

```
flutter pub get
flutter packages pub run build_runner build --delete-conflicting-outputs
```

This command creates the generated files that parse each Record from Firestore into a schema object. Next, run

```
flutter doctor
```

When ready to deploy, use

```
flutter build apk --release
```
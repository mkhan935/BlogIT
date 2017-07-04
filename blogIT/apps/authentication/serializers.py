from django.contrib.auth import authenticate

from rest_framework import serializers

from blogIT.apps.profiles.serializers import ProfileSerializer

from .models import User




class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    #passwords should not be able to be read
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # tokens should not be sent in request so they should not be able to write a token
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all of the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'username', 'password', 'token']

    def create(self, validated_data):
        # Uses the create_user from user to create a new user, i know confusing, read it again.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(max_length=255)
    username = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        # The `validate` method is where you make sure that the current
        # instance of `LoginSerializer` has "valid". In the case of logging a
        # user in, this means validating that they've provided an email
        # and password and that this combination matches one of the users in
        # my database.
        email = data.get('email', None)
        password = data.get('password', None)

        # Raise an exception if an
        # email is not provided.
        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        # Raise an exception if a
        # password is not provided.
        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        # The `authenticate` method is provided by Django and handles checking
        # for a user that matches this email/password combination. In User
        # model, it was set `USERNAME_FIELD` as `email`.
        user = authenticate(username=email, password=password)

        # If no user was found matching this email/password combination then
        # Raise an exception in this case.
        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        # Django provides a flag on our `User` model called `is_active`.
        # this flag tells us whether the user has been banned
        # or otherwise deactivated. Raise an exception in this case.
        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )



        # The `validate` method should return a dictionary of validated data.
        # This is the data that is passed to the `create` and `update` methods
        return {
            'email': user.email,
            'username': user.username,
            'token': user.token
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # When a field should be handled as a serializer, you must explicitly say
    # so. make sure the current serializer cannot read profile information, privacy and security and all.
    profile = ProfileSerializer(write_only=True)

    # get the `bio` and `image` fields from the related Profile
    # model.
    bio = serializers.CharField(source='profile.bio', read_only=True)
    image = serializers.CharField(source='profile.image', read_only=True)

    class Meta:
        model = User
        fields = (
            'email', 'username', 'password', 'token', 'profile', 'bio',
            'image',
        )


        read_only_fields = ('token',)


    def update(self, instance, validated_data):
        """Performs an update on a User."""
        # Django provides a function that handles hashing and
        # salting passwords,remove the password field from the
        # `validated_data` dictionary before iterating over it.
        password = validated_data.pop('password', None)

        # Like passwords, handle profiles separately. To do that,
        # remove the profile data from the `validated_data` dictionary.
        profile_data = validated_data.pop('profile', {})

        for (key, value) in validated_data.items():
            # For the keys remaining in `validated_data`, set them on
            # the current `User` instance one at a time.
            setattr(instance, key, value)

        if password is not None:
            # `.set_password()` is the method mentioned above. It handles all
            # of the security stuff that we shouldn't be concerned with.
            instance.set_password(password)


        instance.save()

        for (key, value) in profile_data.items():
            # same thing but for profiles
            setattr(instance.profile, key, value)

        # Save profile 
        instance.profile.save()

        return instance

import pytest
from torchapp.testing import TorchAppTestCase
from torchapp.examples.image_classifier import ImageClassifier


class TestImageClassifier(TorchAppTestCase):
    app_class = ImageClassifier

    def test_model_incorrect(self):
        app = self.get_app()
        with pytest.raises(ValueError):
            app.model(model_name="resnet1000")

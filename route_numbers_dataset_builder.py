"""route_numbers dataset."""

import tensorflow_datasets as tfds
import tensorflow as tf
from vehicle_info import VehicleInfo
import numpy as np
from PIL import Image, ImageOps

class Builder(tfds.core.GeneratorBasedBuilder):
  """DatasetBuilder for numbers_dataset dataset."""

  VERSION = tfds.core.Version('1.0.0')
  RELEASE_NOTES = {
      '1.0.0': 'Initial release.',
  }

  def split_generators(self, dl_manager):
    return self._split_generators(dl_manager)
  
  def generate_examples(self, **kwargs):
    return self._generate_examples(**kwargs)

  def _info(self) -> tfds.core.DatasetInfo:
    """Returns the dataset metadata."""
    # TODO(numbers_dataset): Specifies the tfds.core.DatasetInfo object
    return self.dataset_info_from_configs(
        features=tfds.features.FeaturesDict({
            # These are the features of your dataset like images, labels ...
            'image': tfds.features.Image(shape=(None, None, 3)),
            'image/filename': tfds.features.Text(),
            'objects': tfds.features.Sequence({
                'bbox': tfds.features.BBoxFeature(),
                'label': tfds.features.ClassLabel(names=['route_number']),
            }),
        }),
        # If there's a common (input, target) tuple from the
        # features, specify them here. They'll be used if
        # `as_supervised=True` in `builder.as_dataset`.
        supervised_keys=('image', 'bbox'),  # Set to `None` to disable
        homepage='https://github.com/transitsense/transitsense-data-pull',
    )

  def _split_generators(self, dl_manager: tfds.download.DownloadManager):
    """Returns SplitGenerators."""
    # TODO(numbers_dataset): Downloads the data and defines the splits
    path = dl_manager.extract('dataset-numbers-split.zip')

    # TODO(numbers_dataset): Returns the Dict[split names, Iterator[Key, Example]]
    return {
        'train': self._generate_examples(path / 'train'),
        'test': self._generate_examples(path / 'test'),
    }

  def _generate_examples(self, path):
    """Yields examples."""
    # TODO(numbers_dataset): Yields (key, example) tuples from the dataset
    csv_path = path / 'vehicle_data.csv'
    with open(csv_path, 'r') as f:
      lines = f.readlines()
      vehicles = [VehicleInfo.from_columns(line.strip().split(',')) for line in lines[1:]]

    images_path = path / 'images'
    for f in images_path.glob('*.jpg'):
      image_filename = f.name
      vehicle = next((v for v in vehicles if v.image_filename == image_filename), None)
      if vehicle is None:
        continue

      image = Image.open(str(f))
      image_width, image_height = image.size
      image = np.array(image)

      yield image_filename, {
        'image': image,
        'image/filename': image_filename,
        'objects': [{
          'bbox': tfds.features.BBox(
            ymin=vehicle.route_number_roi.start.y / image_height,
            xmin=vehicle.route_number_roi.start.x / image_width,
            ymax=vehicle.route_number_roi.end.y / image_height,
            xmax=vehicle.route_number_roi.end.x / image_width,
          ),
          'label': 'route_number',
        }]
      }
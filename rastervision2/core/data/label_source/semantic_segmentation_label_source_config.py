from typing import Optional, Union

from rastervision2.core.data.raster_source import (RasterSourceConfig,
                                                   RasterizedSourceConfig)
from rastervision2.core.data.label_source import (
    LabelSourceConfig, SemanticSegmentationLabelSource)
from rastervision2.core.data.class_config import (ClassConfig)
from rastervision2.pipeline.config import (register_config, Field)


@register_config('semantic_segmentation_label_source')
class SemanticSegmentationLabelSourceConfig(LabelSourceConfig):
    raster_source: Union[RasterSourceConfig, RasterizedSourceConfig] = Field(
        ..., description='The labels in the form of rasters.')
    rgb_class_config: Optional[ClassConfig] = Field(
        None,
        description=
        ('If set, will infer the class_ids for the labels using the colors field. This '
         'assumes the labels are stored as RGB rasters.'))

    def build(self, class_config, crs_transformer, extent, tmp_dir):
        if isinstance(self.raster_source, RasterizedSourceConfig):
            rs = self.raster_source.build(class_config, crs_transformer,
                                          extent)
        else:
            rs = self.raster_source.build(tmp_dir)
        return SemanticSegmentationLabelSource(rs, self.rgb_class_config)

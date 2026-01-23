"""
Pydantic models for error specifications.

This module provides type-safe, validated error specification models
to replace the previous file-based YAML configuration approach.

All default values and references are preserved from the original implementation
in errors.py to maintain consistency with established specifications.
"""

from typing import Dict, List, Optional

from pydantic import BaseModel, ConfigDict, Field


class TGESModel(BaseModel):
    """
    Truncated Gaussian Error Spec (Pydantic Model).

    Represents a truncated Gaussian distribution for error specifications.
    """

    model_config = ConfigDict(validate_assignment=True)

    rms: float = Field(default=0.0, ge=0.0, description="RMS value (must be >= 0)")
    rms_unit: str = Field(
        default="", description="Unit for RMS value (e.g., 'm', 'rad')"
    )
    cutoff: float = Field(
        default=2.0, gt=0.0, description="Cutoff value in sigma (must be > 0)"
    )
    mean: float = Field(default=0.0, description="Mean value of the distribution")


class OffsetSpecModel(BaseModel):
    """2D offset specification model."""

    x: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="X-axis offset specification",
    )
    y: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="Y-axis offset specification",
    )


class OffsetSpec3DModel(BaseModel):
    """3D offset specification model."""

    x: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="X-axis offset specification",
    )
    y: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="Y-axis offset specification",
    )
    z: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="Z-axis offset specification",
    )


class GainSpecModel(BaseModel):
    """Gain specification model."""

    x: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit=""),
        description="X-axis gain specification",
    )
    y: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit=""),
        description="Y-axis gain specification",
    )


class RotationSpecModel(BaseModel):
    """1D rotation specification model (roll only)."""

    roll: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="rad"),
        description="Roll rotation around z-axis",
    )


class RotationSpec3DModel(BaseModel):
    """3D rotation specification model."""

    roll: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="rad"),
        description="Roll rotation around z-axis",
    )
    pitch: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="rad"),
        description="Pitch rotation around x-axis",
    )
    yaw: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="rad"),
        description="Yaw rotation around y-axis",
    )


class NoiseSpecModel(BaseModel):
    """Noise specification model."""

    x: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="X-axis noise specification",
    )
    y: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit="m"),
        description="Y-axis noise specification",
    )


class BPMErrorSpecModel(BaseModel):
    """BPM error specification model."""

    offset: OffsetSpecModel = Field(
        default_factory=OffsetSpecModel, description="Offset error specification"
    )
    gain: GainSpecModel = Field(
        default_factory=GainSpecModel, description="Gain error specification"
    )
    rot: RotationSpecModel = Field(
        default_factory=RotationSpecModel, description="Rotation error specification"
    )
    tbt_noise: NoiseSpecModel = Field(
        default_factory=NoiseSpecModel, description="Turn-by-turn noise specification"
    )
    co_noise: NoiseSpecModel = Field(
        default_factory=NoiseSpecModel, description="Closed orbit noise specification"
    )


class MainMultipoleErrorSpecModel(BaseModel):
    """Main multipole error specification model."""

    fse: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit=""),
        description="Fractional Strength Error specification",
    )


class BendErrorSpecModel(BaseModel):
    """Bend magnet error specification model."""

    offset: OffsetSpecModel = Field(
        default_factory=lambda: OffsetSpecModel(
            x=TGESModel(rms=100e-6, rms_unit="m"),
            y=TGESModel(rms=100e-6, rms_unit="m"),
        ),
        description="2D offset error specification",
    )
    roll: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.5e-3, rms_unit="rad"),
        description="Roll error specification",
    )
    multipole_main_fse: Optional[TGESModel] = Field(
        default=None, description="Main multipole fractional strength error"
    )


# ============================================================================
# Magnet Error Specifications with Inheritance (for Quads, Sexts, Octs)
# ============================================================================


class BaseMagnetErrorSpecModel(BaseModel):
    """
    Base magnet error specification model with common fields.

    All magnet types share offset and roll errors. The main_fse (Fractional
    Strength Error) is defined here with a default of 0.0, and subclasses
    override it with appropriate values from PDR Table 3.1.9.
    """

    offset: OffsetSpecModel = Field(
        default_factory=lambda: OffsetSpecModel(
            x=TGESModel(rms=30e-6, rms_unit="m"),
            y=TGESModel(rms=30e-6, rms_unit="m"),
        ),
        description="2D offset error specification",
    )
    roll: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.2e-3, rms_unit="rad"),
        description="Roll error specification",
    )
    main_fse: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit=""),
        description="Main multipole fractional strength error",
    )


class QuadErrorSpecModel(BaseMagnetErrorSpecModel):
    """
    Quadrupole error specification model.

    Based on NSLS-II PDR Table 3.1.9: FSE = 2.5e-4
    """

    main_fse: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=2.5e-4, rms_unit=""),
        description="Quadrupole fractional strength error (PDR Table 3.1.9)",
    )


class SextErrorSpecModel(BaseMagnetErrorSpecModel):
    """
    Sextupole error specification model.

    Based on NSLS-II PDR Table 3.1.9: FSE = 5e-4
    """

    main_fse: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=5e-4, rms_unit=""),
        description="Sextupole fractional strength error (PDR Table 3.1.9)",
    )


class OctErrorSpecModel(BaseMagnetErrorSpecModel):
    """
    Octupole error specification model.

    FSE = 0.0 (no main field error for octupoles in current specification)
    """

    main_fse: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.0, rms_unit=""),
        description="Octupole fractional strength error",
    )


# Backward compatibility aliases
QuadSextErrorSpecModel = BaseMagnetErrorSpecModel
QuadNonlinMagnetErrorSpecModel = BaseMagnetErrorSpecModel


class GirderErrorSpecModel(BaseModel):
    """
    Girder support error specification model.

    Girders have upstream (us) and downstream (ds) offset specifications,
    each with x, y, z components (3D offset).
    """

    us_offset: OffsetSpec3DModel = Field(
        default_factory=lambda: OffsetSpec3DModel(
            x=TGESModel(rms=100e-6, rms_unit="m"),
            y=TGESModel(rms=100e-6, rms_unit="m"),
        ),
        description="Upstream offset error specification (3D)",
    )
    ds_offset: OffsetSpec3DModel = Field(
        default_factory=lambda: OffsetSpec3DModel(
            x=TGESModel(rms=100e-6, rms_unit="m"),
            y=TGESModel(rms=100e-6, rms_unit="m"),
        ),
        description="Downstream offset error specification (3D)",
    )
    roll: TGESModel = Field(
        default_factory=lambda: TGESModel(rms=0.5e-3, rms_unit="rad"),
        description="Roll error specification",
    )
    chain_constraints: Optional[List] = Field(
        default=None, description="Chain constraints for girders"
    )


# ============================================================================
# NSLS2 (Current NSLS-II) Error Specification Model
# ============================================================================


class NSLS2ErrorSpecModel(BaseModel):
    """
    Complete error specification model for NSLS2 (current NSLS-II) facility.

    This model contains all error specifications needed for the facility,
    organized by component type.

    References:
    - NSLS-II PDR (Preliminary Design Report) Tables 3.1.4, 3.1.8, 3.1.9
    - ~/git_repos/nsls2scripts3/SDDS_multipoles/mpole_err_spec/CD3_mpole_spec.txt
    """

    bpms: BPMErrorSpecModel = Field(
        default_factory=lambda: BPMErrorSpecModel(
            # Some (not all) based on NSLS-II PDR Table 3.1.4
            offset=OffsetSpecModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            gain=GainSpecModel(
                x=TGESModel(rms=5e-2, rms_unit="", cutoff=2.0),
                y=TGESModel(rms=5e-2, rms_unit="", cutoff=2.0),
            ),
            rot=RotationSpecModel(
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0)
            ),
            tbt_noise=NoiseSpecModel(
                x=TGESModel(rms=3e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=3e-6, rms_unit="m", cutoff=2.0),
            ),
            co_noise=NoiseSpecModel(
                x=TGESModel(rms=0.1e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=0.1e-6, rms_unit="m", cutoff=2.0),
            ),
        ),
        description="BPM error specifications",
    )

    bends: BendErrorSpecModel = Field(
        default_factory=lambda: BendErrorSpecModel(
            # Based on NSLS-II PDR Table 3.1.8 (and 3.1.4)
            offset=OffsetSpecModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            roll=TGESModel(rms=0.5e-3, rms_unit="rad", cutoff=2.0),
        ),
        description="Bend magnet error specifications",
    )

    quads_sexts: Dict[str, BaseMagnetErrorSpecModel] = Field(
        default_factory=lambda: {
            # Based on NSLS-II PDR Table 3.1.9 (main FSE)
            # Based on NSLS-II PDR Table 3.1.8 (and 3.1.4) (offset and roll)
            "QUAD": QuadErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 2.5e-4 from QuadErrorSpecModel
            ),
            "HIQUAD": QuadErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 2.5e-4 from QuadErrorSpecModel
            ),
            "SEXT": SextErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 5e-4 from SextErrorSpecModel
            ),
            "HISEXT": SextErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 5e-4 from SextErrorSpecModel
            ),
        },
        description="Quad and sextupole error specifications by magnet type",
    )

    girders: GirderErrorSpecModel = Field(
        default_factory=lambda: GirderErrorSpecModel(
            # Based on NSLS-II PDR Table 3.1.8
            us_offset=OffsetSpec3DModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            ds_offset=OffsetSpec3DModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            roll=TGESModel(rms=0.5e-3, rms_unit="rad", cutoff=2.0),
            chain_constraints=None,
        ),
        description="Girder support error specifications",
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True  # Validate on attribute assignment
        arbitrary_types_allowed = False


# ============================================================================
# NSLS2U (NSLS-II Upgrade) Error Specification Model
# ============================================================================


class NSLS2UErrorSpecModel(BaseModel):
    """
    Complete error specification model for NSLS2-II Upgrade facility.

    This model contains all error specifications needed for the facility,
    organized by component type.

    References:
    - Some (not all) based on NSLS-II PDR Table 3.1.4
    - ELEGANT: normal = "an", skew = "bn"
    - Tracy: normal = "Bn", skew = "An" (Note: sign of "An" is opposite from "bn")
    """

    bpms: BPMErrorSpecModel = Field(
        default_factory=lambda: BPMErrorSpecModel(
            # Some (not all) based on NSLS-II PDR Table 3.1.4
            offset=OffsetSpecModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=1.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=1.0),
            ),
            gain=GainSpecModel(
                x=TGESModel(rms=5e-2, rms_unit="", cutoff=1.0),
                y=TGESModel(rms=5e-2, rms_unit="", cutoff=1.0),
            ),
            rot=RotationSpecModel(
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=1.0)
            ),
            tbt_noise=NoiseSpecModel(
                x=TGESModel(rms=3e-6, rms_unit="m", cutoff=1.0),
                y=TGESModel(rms=3e-6, rms_unit="m", cutoff=1.0),
            ),
            co_noise=NoiseSpecModel(
                x=TGESModel(rms=0.1e-6, rms_unit="m", cutoff=1.0),
                y=TGESModel(rms=0.1e-6, rms_unit="m", cutoff=1.0),
            ),
        ),
        description="BPM error specifications",
    )

    bends: BendErrorSpecModel = Field(
        default_factory=lambda: BendErrorSpecModel(
            # Default values (can be overridden)
            offset=OffsetSpecModel(
                x=TGESModel(rms=15e-6, rms_unit="m", cutoff=1.0),
                y=TGESModel(rms=15e-6, rms_unit="m", cutoff=1.0),
            ),
            roll=TGESModel(rms=0.1e-3, rms_unit="rad", cutoff=1.0),
            multipole_main_fse=TGESModel(rms=1e-3, rms_unit="", cutoff=1.0),
        ),
        description="Bend magnet error specifications (PMQ)",
    )

    quads_nonlin_magnets: Dict[str, BaseMagnetErrorSpecModel] = Field(
        default_factory=lambda: {
            # Based on NSLS-II PDR Table 3.1.9 (main FSE)
            # Based on NSLS-II PDR Table 3.1.8 (and 3.1.4) (offset and roll)
            "EM_QUAD": QuadErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=1.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=1.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=1.0),
                # main_fse defaults to 2.5e-4 from QuadErrorSpecModel
            ),
            "SEXT": SextErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=1.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=1.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=1.0),
                # main_fse defaults to 5e-4 from SextErrorSpecModel
            ),
            "OCT": OctErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=1.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=1.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=1.0),
                # main_fse defaults to 0.0 from OctErrorSpecModel
            ),
        },
        description="Quad and nonlinear magnet error specifications by magnet type",
    )

    girders: GirderErrorSpecModel = Field(
        default_factory=lambda: GirderErrorSpecModel(
            us_offset=OffsetSpec3DModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=1.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=1.0),
            ),
            ds_offset=OffsetSpec3DModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=1.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=1.0),
            ),
            roll=TGESModel(rms=0.5e-3, rms_unit="rad", cutoff=1.0),
            chain_constraints=None,
        ),
        description="Girder support error specifications",
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True  # Validate on attribute assignment
        arbitrary_types_allowed = False


# ============================================================================
# NSLS2CB (NSLS-II with Complex Bends) Error Specification Model
# ============================================================================


class NSLS2CBErrorSpecModel(BaseModel):
    """
    Complete error specification model for NSLS2 with Complex Bends facility.

    This model contains all error specifications needed for the facility,
    organized by component type.

    References:
    - NSLS-II PDR (Preliminary Design Report) Tables 3.1.4, 3.1.8, 3.1.9
    - ~/git_repos/nsls2scripts3/SDDS_multipoles/mpole_err_spec/CD3_mpole_spec.txt
    - CD3-SYSMULT.QUAD, CD3-RDMMULT.QUAD
    - CD3-SYSMULT.HIQUAD, CD3-RDMMULT.HIQUAD
    - CD3-SYSMULT.SEXT, CD3-RDMMULT.SEXT
    - CD3-SYSMULT.HISEXT, CD3-RDMMULT.HISEXT

    Note:
    - ELEGANT: normal = "an", skew = "bn"
    - Tracy: normal = "Bn", skew = "An" (sign of "An" is opposite from "bn")
    """

    bpms: BPMErrorSpecModel = Field(
        default_factory=lambda: BPMErrorSpecModel(
            # Some (not all) based on NSLS-II PDR Table 3.1.4
            offset=OffsetSpecModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            gain=GainSpecModel(
                x=TGESModel(rms=5e-2, rms_unit="", cutoff=2.0),
                y=TGESModel(rms=5e-2, rms_unit="", cutoff=2.0),
            ),
            rot=RotationSpecModel(
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0)
            ),
            tbt_noise=NoiseSpecModel(
                x=TGESModel(rms=3e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=3e-6, rms_unit="m", cutoff=2.0),
            ),
            co_noise=NoiseSpecModel(
                x=TGESModel(rms=0.1e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=0.1e-6, rms_unit="m", cutoff=2.0),
            ),
        ),
        description="BPM error specifications",
    )

    bends: BendErrorSpecModel = Field(
        default_factory=lambda: BendErrorSpecModel(
            # Based on NSLS-II PDR Table 3.1.8 (and 3.1.4)
            offset=OffsetSpecModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            roll=TGESModel(rms=0.5e-3, rms_unit="rad", cutoff=2.0),
        ),
        description="Bend magnet error specifications",
    )

    quads_sexts: Dict[str, BaseMagnetErrorSpecModel] = Field(
        default_factory=lambda: {
            # Based on NSLS-II PDR Table 3.1.9 (main FSE)
            # Based on NSLS-II PDR Table 3.1.8 (and 3.1.4) (offset and roll)
            "QUAD": QuadErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 2.5e-4 from QuadErrorSpecModel
            ),
            "HIQUAD": QuadErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 2.5e-4 from QuadErrorSpecModel
            ),
            "SEXT": SextErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 5e-4 from SextErrorSpecModel
            ),
            "HISEXT": SextErrorSpecModel(
                offset=OffsetSpecModel(
                    x=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                    y=TGESModel(rms=30e-6, rms_unit="m", cutoff=2.0),
                ),
                roll=TGESModel(rms=0.2e-3, rms_unit="rad", cutoff=2.0),
                # main_fse defaults to 5e-4 from SextErrorSpecModel
            ),
        },
        description="Quad and sextupole error specifications by magnet type",
    )

    girders: GirderErrorSpecModel = Field(
        default_factory=lambda: GirderErrorSpecModel(
            # Based on NSLS-II PDR Table 3.1.8
            us_offset=OffsetSpec3DModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            ds_offset=OffsetSpec3DModel(
                x=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
                y=TGESModel(rms=100e-6, rms_unit="m", cutoff=2.0),
            ),
            roll=TGESModel(rms=0.5e-3, rms_unit="rad", cutoff=2.0),
            chain_constraints=None,
        ),
        description="Girder support error specifications",
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True  # Validate on attribute assignment
        arbitrary_types_allowed = False

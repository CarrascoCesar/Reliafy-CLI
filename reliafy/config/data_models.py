# Copyright by Dr. Cesar Carrasco, (2025)
from enum import StrEnum
from typing import ClassVar, Tuple

import numpy as np
from matplotlib import cm, colors
from pydantic import BaseModel, ConfigDict, Field, ValidationInfo, field_validator


class RunTypeEnum(StrEnum):
    design = "design"
    analyze = "analyze"
    simulate = "simulate"


class IsMethodEnum(StrEnum):
    mpp_normal = "mpp_normal"
    kde = "kde"
    mixture = "mixture"
    mcmc = "mcmc"


class MCMCFitMethodEnum(StrEnum):
    kde = "kde"
    mixture = "mixture"


class KDEBandwidthMethodEnum(StrEnum):
    scott = "scott"
    silverman = "silverman"


class MixtureCovTypeEnum(StrEnum):
    full = "full"
    tied = "tied"
    diag = "diag"
    spherical = "spherical"


class ScipyMethodEnum(StrEnum):
    SLSQP = "SLSQP"
    COBYLA = "COBYLA"
    trust_constr = "trust-constr"
    newton = "newton"
    secant = "secant"


class SORMethodEnum(StrEnum):
    Breitung = "Breitung"
    Tvedt3T = "Tvedt3T"
    TvedtSI = "TvedtSI"
    TvedtDI = "TvedtDI"
    Hohenbichler = "Hohenbichler"
    Koyluoglu = "Koyluoglu"
    ZhaoEmpirical = "ZhaoEmpirical"
    SOSPA_L = "SOSPA_L"
    SOSPA_H = "SOSPA_H"
    IFFT = "IFFT"


class SORApproximationEnum(StrEnum):
    Paraboloid = "Paraboloid"
    Taylor2 = "Taylor2"


class SORFitMethodEnum(StrEnum):
    FiniteDiff = "FiniteDiff"
    ZhaoPF = "ZhaoPF"
    Kiureghian = "Kiureghian"
    SR1 = "SR1"
    AnalyticAll = "AnalyticAll"
    # AnalyticGrad = "AnalyticGrad"


class SORFiniteDiffMethodEnum(StrEnum):
    central = "central"
    forward = "forward"
    backward = "backward"


class DiffsCheckMethodEnum(StrEnum):
    central = "central"
    forward = "forward"
    backward = "backward"
    complex = "complex"


class SORFiniteDiffHessFormEnum(StrEnum):
    full = "full"
    diagonal = "diagonal"


class PlotType(StrEnum):
    contour = "contour"
    surface = "surface"


class AlphaDirectionEnum(StrEnum):
    outward = "outward"
    inward = "inward"


class DesignTypeEnum(StrEnum):
    WithObjective = "WithObjective"
    InverseSORM = "InverseSORM"
    InverseFORM = "InverseFORM"


class BaseEnumModel(BaseModel):
    @classmethod
    def validate_str_enum_field(cls, value: str, info: ValidationInfo, enum_class: StrEnum) -> str:
        """
        Checks if the field value is valid and converts it to appropriate case.
        Accepts both enum names (case-insensitive) and values.
        """
        valid_options = list(enum_class.__members__)
        if isinstance(value, enum_class):
            return value.name
        if not isinstance(value, str):
            raise ValueError(f"{info.field_name} must be a string or one of: {valid_options}. Got: {type(value)}")
        # Try to match by name (case-insensitive)
        for option in valid_options:
            if option.lower() == value.lower().strip():
                return option
        # Try to match by value
        for option in valid_options:
            if getattr(enum_class, option).value == value:
                return option
        raise ValueError(
            f"{info.field_name} must be one of: {valid_options} (case-insensitive names or values). Got: {value}"
        )


# fmt: off
class RunConfiguration(BaseEnumModel):
    """
    Class representing the configuration for a simulation.
    It defines whether an analysis or design simulation should be run and whether to include Monte Carlo simulations.
    It also defines whether to plot the reliability based failure assessment diagram (RFAD), the limit state function (LSF),
    and the probability density functions (PDFs) of the stochastic variables.

    Attributes:
    -----------
    run_type: Literal["design", "analysis"]
        The type of run to perform. It can be either 'design' or 'analysis'. Default is 'analysis'.
    include_sorm: bool
        A flag indicating whether to include second order reliability method (SORM) in the run. Default is False.
    include_mc: bool
        A flag indicating whether to include Monte Carlo simulations in the run. Default is False.
    include_form: bool
        A flag indicating whether to include first order reliability method (FORM) simulations in the run. Default is False.
    mc_with_is: bool
        A flag indicating whether to use importance sampling with Monte Carlo simulations. Default is False.
    plot_pdfs: bool
        A flag indicating whether to plot the probability density functions (PDFs) of the stochastic variables. Default is False.
    plot_lsf: bool
        A flag indicating whether to plot the limit state function. Default is False.
    plot_rfad: bool
        A flag indicating whether to plot the reliability based failure assessment diagram (RFAD). Default is False.
    api_version: str
        The version of the API being used.
    """
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    run_type: RunTypeEnum = Field(default=RunTypeEnum.analyze)
    include_sorm: bool = Field(default=False)
    include_mc: bool = Field(default=False)
    include_form: bool = Field(default=False)
    mc_with_is: bool = Field(default=False)
    plot_rfad: bool = Field(default=False)
    plot_lsf: bool = Field(default=False)
    plot_pdfs: bool = Field(default=False)

    api_version: str = Field(default="0.1.0", exclude=True)

    @field_validator("run_type", mode="before")
    @classmethod
    def validate_simulation_type(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, RunTypeEnum)
    
    @field_validator('api_version')
    @classmethod
    def validate_api_version(cls, v):
        supported_versions = ["0.1.0"]  # Add new versions here
        if v not in supported_versions:
            raise ValueError(f"Unsupported API version: {v}. Supported: {supported_versions}")
        return v    
    
    # @model_validator(mode='after')
    # def handle_version_compatibility(self):
    #     """Handle version-specific logic and migrations"""
    #     if self.api_version == "1.0.0":
    #         # v1.0.0 clients won't send new_feature_v1_1, it gets the default False
    #         if hasattr(self, 'new_feature_v1_1') and self.new_feature_v1_1 is not False:
    #             logger.warning(f"new_feature_v1_1 not supported in API v1.0.0, ignoring")
    #             self.new_feature_v1_1 = False
        
    #     return self    

class ReliabilityOptions(BaseEnumModel):
    """
    Options for reliability calculations and related numerical settings.

    This model collects tolerances, algorithm choices, finite-difference settings,
    plotting flags, Monte Carlo controls and various checks used across FORM,
    SORM, inverse problems and design optimization routines.

    Key fields (type and brief meaning):
    - form_xtol: float
        Tolerance for FORM termination (variable changes). Range: [1e-8, 1e-2]. Default: 1e-4.
    - form_gtol: float
        Tolerance for FORM termination (Lagrangian gradient norm changes). Range: [1e-8, 1e-2]. Default: 1e-4.
    - form_maxiter: int
        Maximum iterations for FORM. Range: [1, ∞). Default: 1000.
    - form_random_start: bool
        Use a random starting point for FORM/Inverse FORM. Default: False.
    - form_seed: int | None
        Random seed for FORM/Inverse FORM random starts. Default: None.
    - form_max_beta: float (excluded from public serialization)
        Maximum reliability index allowed during FORM/Inverse FORM runs. Also used in design optimization and MC simulations. Range: [2.0, 12.0]. Default: 10.0.
    - design_xtol: float
        Tolerance for design optimization termination (variable changes). Range: [1e-8, 1e-2]. Default: 1e-3.
    - design_gtol: float
        Tolerance for design optimization termination (Lagrangian gradient norm changes). Range: [1e-8, 1e-2]. Default: 1e-3.
    - design_maxiter: int
        Maximum iterations for design optimization. Range: [1, ∞). Default: 1000.
    - design_random_start: bool
        Use a random starting point for design optimization. Default: False.
    - design_seed: int | None
        Random seed for design optimization random starts. Default: None.    
    - max_minimize_attempts: int (excluded from public serialization)
        Maximum attempts when calling the minimizer. Range: [1, 12]. Default: 8.
    - max_workers: int (excluded from public serialization)
        Number of parallel workers (-1 means auto). Range: [-1, 12]. Default: 2.
    - alpha_direction: AlphaDirectionEnum
        Direction convention for alpha (outward / inward). Default: outward.
    - use_nearest_correlation: bool
        Use nearest PSD correlation representation for stochastic variables. Default: False.
    - sor_method: SORMethodEnum
        SORM method to use (Breitung, Tvedt3T, TvedtSI, TvedtDI, Hohenbichler, Koyluoglu, ZhaoEmpirical, SOSPA_L, SOSPA_H, IFFT). Default: SOSPA_H.
    - sor_approximation: SORApproximationEnum
        SORM approximation type (Paraboloid or Taylor2). Default: Taylor2.
    - sor_fit_method: SORFitMethodEnum | None
        Method for SORM limit state function fitting (FiniteDiff, ZhaoPF, Kiureghian, SR1, AnalyticAll; None = auto). Default: None.
    - sor_fit_delta_factor: float
        Factor to scale delta when numerically estimating SORM fit parameters for ZhaoPF and Kiureghian methods. Range: [0.1, 10.0]. Default: 1.0.
    - sor_fdm: SORFiniteDiffMethodEnum
        Finite-difference method for gradient and Hessian (central / forward / backward). Default: forward.
    - sor_fdm_hess_form: SORFiniteDiffHessFormEnum
        Hessian form for finite-difference approximation (full / diagonal). Default: full.
    - check_lsf_diffs_wrtx: bool
        Validate user-provided LSF derivatives against numerical diffs w.r.t. real-space variables. Default: False.
    - check_lsf_diffs_wrtu: bool
        Validate user-provided LSF derivatives against numerical diffs w.r.t. standard-normal (U-space) variables. Default: True.
    - lsf_diffs_check_method: DiffsCheckMethodEnum
        Method for LSF derivative checks (central / forward / backward / complex). Default: forward.
    - check_varscf_diffs_wrtx: bool
        Validate user-provided stochastic variables constraints (real-space). Default: False.
    - check_varscf_diffs_wrtu: bool
        Validate user-provided stochastic variables constraints (U-space). Default: True.
    - varscf_diffs_check_method: DiffsCheckMethodEnum
        Method for stochastic variables constraint derivative checks. Default: forward.
    - check_dof_diffs: bool
        Validate user-provided design objective function derivatives against numerical diffs. Default: True.
    - dof_diffs_check_method: DiffsCheckMethodEnum
        Method for design objective function derivative checks. Default: forward.
    - check_dcf_diffs: bool
        Validate user-provided design constraint function derivatives against numerical diffs. Default: True.
    - dcf_diffs_check_method: DiffsCheckMethodEnum
        Method for design constraint function derivative checks. Default: forward.
    - ifft_std_domain: float
        Standard deviations covered when computing IFFT of characteristic functions. Range: [2, 24]. Default: 16.0.
    - ifft_n: int
        Number of points used in IFFT (power-of-two constrained, 2^8 to 2^16). Default: 4096 (2^12).
    - plot_ifft_funcs: bool
        Generate diagnostic plots for IFFT operations. Default: True.
    - plot_sospa_funcs: bool
        Generate diagnostic plots for SOSPA characteristic functions and derivatives. Default: True.
    - force_curvatures: bool
        Force curvature computations even if not strictly required by selected SORM options. Default: False.
    - qn_epsilon: float
        Tolerance used by quasi-Newton routines. Range: [1e-8, 1e-2]. Default: 1e-8.
    - mc_n: float | None
        Monte Carlo sample size (None means automatic). Must be in [1e3, 1e8] if specified. Default: None.
    - mc_n_max: float (excluded from public serialization)
        Maximum allowed MC samples. Range: [1e3, 1e8]. Default: 1e7.
    - mc_n_min: float (excluded from public serialization)
        Minimum allowed MC samples. Range: [1e3, 1e7]. Default: 1e3.
    - mc_n_min_per_cycle: float (excluded from public serialization)
        Minimum MC samples per cycle when using cycle-based MC stopping. Range: [1e2, 1e7]. Default: 1e3.
    - mc_max_cv: float
        Maximum coefficient of variation per MC estimate allowed. Range: [0.01, 1.0]. Default: 0.05.
    - mc_seed: int | None
        Random seed for Monte Carlo simulations. Default: None.
    - mc_remove_oob: bool
        Remove out-of-bounds samples during MC simulation (bounds or constraint violations). Default: True.
    - mc_min_cycles: int (excluded from public serialization)
        Minimum MC cycles when using cycle-based MC stopping. Range: [1, 10]. Default: 3.
    - mc_max_cycles: int (excluded from public serialization)
        Maximum MC cycles when using cycle-based MC stopping. Range: [1, 1000]. Default: 500.
    - mc_max_mb_per_cycle: int (excluded from public serialization)
        Maximum memory (MB) per MC cycle. Range: [1, 1000]. Default: 100.
    - is_method: IsMethodEnum
        Importance sampling proposal method (kde / mixture / mcmc / mpp_normal). Default: kde.
    - is_kde_bandwidth: KDEBandwidthMethodEnum | float
        Bandwidth selection method for KDE (scott / silverman) or positive numeric value. Default: scott.
    - is_mixture_components: int
        Number of mixture components for mixture IS methods. Range: [1, 16]. Default: 6.
    - is_mixture_cov_type: MixtureCovTypeEnum
        Covariance type for mixture IS methods (full / tied / diag / spherical). Default: full.
    - is_fit_samples: int
        Number of samples to collect for fitting the proposal distribution (for KDE and mixture IS). Range: [100, 100000]. Default: 2000.
    - is_mcmc_chains: int
        Number of parallel Metropolis chains to run during MCMC proposal fitting. Range: [1, 100]. Default: 5.
    - is_mcmc_chain_length: int
        Length of each MCMC chain during proposal fitting. Range: [100, 10000]. Default: 500.
    - is_mcmc_thinning: int
        Thinning factor for MCMC chains during proposal fitting. Range: [1, 100]. Default: 3.
    - is_mcmc_burnin: int
        Number of samples to discard as burn-in during MCMC proposal fitting. Range: [100, 1000]. Default: 200.
    - is_mcmc_fit_method: MCMCFitMethodEnum
        Method used to fit the MCMC proposal distribution (kde / mixture). Default: kde.

    Notes:
    - Many enum-style fields accept either the enum member name (case-insensitive)
      or the enum value; validators normalize to the enum name.
    - Several fields are intentionally excluded from serialization (exclude=True)
      because they are internal runtime controls rather than part of the public API.
    - All range constraints are enforced at the Pydantic validation level.
    """
    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    PROFILE_GROUPS: ClassVar[tuple[tuple[str, tuple[str, ...]], ...]] = (
        ("FORM", ("form_xtol", "form_gtol", "form_maxiter", "form_random_start", "form_seed")),
        ("Design", ("design_xtol", "design_gtol", "design_maxiter", "design_random_start", "design_seed")),
        ("General", ("alpha_direction", "use_nearest_correlation")),
        (
            "SORM",
            (
                "sor_method",
                "sor_approximation",
                "sor_fit_method",
                "sor_fit_delta_factor",
                "sor_fdm",
                "sor_fdm_hess_form",
                "force_curvatures",
                "qn_epsilon",
            ),
        ),
        ("IFFT", ("ifft_std_domain", "ifft_n", "plot_ifft_funcs")),
        ("SOSPA", ("plot_sospa_funcs",)),
        (
            "Derivative checking",
            (
                "check_lsf_diffs_wrtx",
                "check_lsf_diffs_wrtu",
                "lsf_diffs_check_method",
                "check_varscf_diffs_wrtx",
                "check_varscf_diffs_wrtu",
                "varscf_diffs_check_method",
                "check_dof_diffs",
                "dof_diffs_check_method",
                "check_dcf_diffs",
                "dcf_diffs_check_method",
            ),
        ),
        ("Monte Carlo", ("mc_n", "mc_max_cv", "mc_seed", "mc_remove_oob")),
        (
            "Importance Sampling",
            (
                "is_method",
                "is_kde_bandwidth",
                "is_mixture_components",
                "is_mixture_cov_type",
                "is_fit_samples",
                "is_mcmc_chains",
                "is_mcmc_chain_length",
                "is_mcmc_thinning",
                "is_mcmc_burnin",
                "is_mcmc_fit_method",
            ),
        ),
    )

    form_xtol: float = Field(default=1e-4, ge=1e-8, le=1e-2)
    form_gtol: float = Field(default=1e-4, ge=1e-8, le=1e-2)
    form_maxiter: int = Field(default=1000, ge=1)
    form_random_start: bool = Field(default=False)
    form_seed: int | None = Field(default=None)
    form_max_beta : float = Field(default=10.0, ge=2.0, le=12.0, exclude=True)
    design_xtol: float = Field(default=1e-3, ge=1e-8, le=1e-2)
    design_gtol: float = Field(default=1e-3, ge=1e-8, le=1e-2)
    design_maxiter: int = Field(default=1000, ge=1)
    design_random_start: bool = Field(default=False)
    design_seed: int | None = Field(default=None)
    max_minimize_attempts: int = Field(default=8, ge=1, le=12, exclude=True)
    max_workers: int = Field(default=2, ge=-1, le=12, exclude=True)
    alpha_direction: AlphaDirectionEnum = Field(default=AlphaDirectionEnum.outward)
    use_nearest_correlation: bool = Field(default=False)
    sor_method: SORMethodEnum = Field(default=SORMethodEnum.SOSPA_H)
    sor_approximation: SORApproximationEnum = Field(default=SORApproximationEnum.Paraboloid)
    sor_fit_method: SORFitMethodEnum | None = Field(default=None)
    sor_fit_delta_factor: float = Field(default=1.0, ge=0.1, le=10.0)
    sor_fdm: SORFiniteDiffMethodEnum = Field(default=SORFiniteDiffMethodEnum.forward)
    sor_fdm_hess_form: SORFiniteDiffHessFormEnum = Field(default=SORFiniteDiffHessFormEnum.full)
    check_lsf_diffs_wrtx: bool = Field(default = False)
    check_lsf_diffs_wrtu: bool = Field(default = True)
    lsf_diffs_check_method: DiffsCheckMethodEnum = Field(default=DiffsCheckMethodEnum.forward)
    check_varscf_diffs_wrtx: bool = Field(default = False)
    check_varscf_diffs_wrtu: bool = Field(default = True)
    varscf_diffs_check_method: DiffsCheckMethodEnum = Field(default=DiffsCheckMethodEnum.forward)
    check_dof_diffs: bool = Field(default = True)
    dof_diffs_check_method: DiffsCheckMethodEnum = Field(default=DiffsCheckMethodEnum.forward)
    check_dcf_diffs: bool = Field(default = True)
    dcf_diffs_check_method: DiffsCheckMethodEnum = Field(default=DiffsCheckMethodEnum.forward)
    ifft_std_domain: float = Field(default=16.0, ge=2, le=24)
    ifft_n: int = Field(default=2**12)
    plot_ifft_funcs: bool = Field(default = True)
    plot_sospa_funcs: bool = Field(default = True)
    force_curvatures: bool = Field(default = False)
    qn_epsilon: float = Field(default=1e-8, ge=1e-8, le=1e-2)
    mc_n: float | None = Field(default=None)
    mc_n_max: float = Field(default=5e8, ge=1e3, le=1e9, exclude=True)
    mc_n_min: float = Field(default=1e3, ge=1e3, le=1e7, exclude=True)
    mc_n_min_per_cycle: float = Field(default=1e3, ge=1e2, le=1e7, exclude=True)    
    mc_max_cv: float = Field(default=0.05, ge=0.01, le=1)
    mc_seed: int | None = Field(default=None)
    mc_remove_oob: bool = Field(default=True)
    mc_min_cycles: int = Field(default=3, ge=1, le=10, exclude=True)
    mc_max_cycles: int = Field(default=500, ge=1, le=1000, exclude=True)
    mc_max_mb_per_cycle: int = Field(default=400, ge=1, le=1000, exclude=True)    
    is_method: IsMethodEnum = Field(default=IsMethodEnum.kde)
    is_kde_bandwidth: KDEBandwidthMethodEnum | float = Field(default=KDEBandwidthMethodEnum.scott)
    is_mixture_components: int = Field(default=6, ge=1, le=16)
    is_mixture_cov_type: MixtureCovTypeEnum = Field(default=MixtureCovTypeEnum.full)
    is_fit_samples: int = Field(default=2000, ge=100, le=100000)
    is_mcmc_chains: int = Field(default=5, ge=1, le=100)
    is_mcmc_chain_length: int = Field(default=500, ge=100, le=10000)
    is_mcmc_thinning: int = Field(default=3, ge=1, le=100)
    is_mcmc_burnin: int = Field(default=200, ge=100, le=1000)
    is_mcmc_fit_method: MCMCFitMethodEnum = Field(default=MCMCFitMethodEnum.kde)
    

    @field_validator("sor_method", mode="before")
    @classmethod
    def validate_sor_method(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, SORMethodEnum)

    @field_validator("sor_approximation", mode="before")
    @classmethod
    def validate_sor_approximation(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, SORApproximationEnum)

    @field_validator("sor_fit_method", mode="before")
    @classmethod
    def validate_sor_fit_method(cls, v: str, info: ValidationInfo) -> str:
        if v is None:
            return None
        return cls.validate_str_enum_field(v, info, SORFitMethodEnum)

    @field_validator("sor_fdm", mode="before")
    @classmethod
    def validate_sor_fdm(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, SORFiniteDiffMethodEnum)

    @field_validator("sor_fdm_hess_form", mode="before")
    @classmethod
    def validate_fdm_hess_form(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, SORFiniteDiffHessFormEnum)

    @field_validator("lsf_diffs_check_method", mode="before")
    @classmethod
    def validate_lsf_diffs_check_method(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, DiffsCheckMethodEnum)

    @field_validator("dof_diffs_check_method", mode="before")
    @classmethod
    def validate_dof_diffs_check_method(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, DiffsCheckMethodEnum)
    
    @field_validator("dcf_diffs_check_method", mode="before")
    @classmethod
    def validate_dcf_diffs_check_method(cls, v: str, info: ValidationInfo) -> str:
        return cls.validate_str_enum_field(v, info, DiffsCheckMethodEnum)
    
    @field_validator("ifft_n", mode="before")
    @classmethod
    def validate_ifft_n(cls, v, info: ValidationInfo) -> int:
        if v < 2**8 or v > 2**16 or (v & (v - 1)) != 0:
            raise ValueError(f"{info.field_name} must be a power-of-two between 2**8 and 2**16. Got: {v}")
        return v    
    
    @field_validator("mc_n", mode="before")
    @classmethod
    def validate_mc_n(cls, v, info):
        if v is None:
            return None
        if isinstance(v, (int, float)):
            if not (1e3 <= float(v) <= 1e8):
                raise ValueError(f"{info.field_name} must be between 1e3 and 1e8 or 'auto'. Got: {v!r}")
            return float(v)
        raise ValueError(f"{info.field_name} must be a float or None. Got: {v!r}")

    @field_validator("is_kde_bandwidth", mode="before")
    @classmethod
    def validate_is_kde_bandwidth(cls, v, info: ValidationInfo):
        if isinstance(v, (int, float)):
            if v <= 0:
                raise ValueError(f"{info.field_name} must be positive when specified as a number. Got: {v}")
            return float(v)
        return cls.validate_str_enum_field(v, info, KDEBandwidthMethodEnum)


def validate_cmap(value: str | list | np.ndarray, key: str) -> str | list:
    """
    Validates that the input is either a valid matplotlib colormap name (string)
    or a list of RGBA values with shape (n, 4), where 1 <= n <= 256.

    Args:
        value: The colormap specification (str, list or np.ndarray).
        key: The context key for error messages.

    Returns:
        The validated colormap name or list.

    Raises:
        ValueError: If the input is not a valid colormap.
    """
    if isinstance(value, (list, np.ndarray)):
        arr = np.array(value, dtype=float)
        if arr.ndim != 2 or arr.shape[1] != 4 or not (1 <= arr.shape[0] <= 256):
            raise ValueError(f"{key} cmap must be a list of shape (n, 4) where 1 <= n <= 256.")

        if np.any(arr < 0) or np.any(arr > 1):
            raise ValueError(f"{key} cmap RGBA values must be in the range [0, 1].")
        try:
            colors.ListedColormap(arr)
            return arr.tolist()
        except Exception as e:
            raise ValueError(f"{key} cmap must be a valid list for ListedColormap: {e}")

    if isinstance(value, str):
        try:
            cm.get_cmap(value)
            return value
        except Exception:
            raise ValueError(f"{key} cmap '{value}' is not a valid matplotlib colormap name.")
    raise ValueError(
        f"{key} cmap must be a valid matplotlib colormap name or a list of shape (n, 4) with RGBA values in [0, 1]."
    )


def validate_view(value: str | Tuple[float, float, float], key: str) -> str | Tuple[float, float, float]:
    """
    Validates that the input is either a valid view string or a tuple of three floats.

    Args:
        value: The view specification (str or tuple).
        key: The context key for error messages.

    Returns:
        The validated view string (with canonical capitalization) or tuple of floats.

    Raises:
        ValueError: If the input is not a valid view.
    """
    allowed_strings = ["auto", "default", "XY", "XZ", "YZ", "-XZ", "-YZ", "-XY"]
    if isinstance(value, str):
        value_stripped = value.strip().lower()
        for allowed in allowed_strings:
            if value_stripped == allowed.lower():
                return allowed
        raise ValueError(
            f"{key} view must be one of {allowed_strings} (case-insensitive) or a tuple of three floats. Got: {value!r}"
        )
    if isinstance(value, (tuple, list)) and len(value) == 3 and all(isinstance(v, (float, int)) for v in value):
        return tuple(float(v) for v in value)
    raise ValueError(
        f"{key} view must be one of {allowed_strings} (case-insensitive) or a tuple of three floats. Got: {value!r}"
    )


class RFADoptions(BaseModel):
    """
    Options for Reliability-based Failure Assessment Diagram (RFAD) visualization.

    Attributes:
    -----------
    n_x_points: int
        Number of grid points along the first variable axis. Range: [5, 60]. Default: 30.
    n_y_points: int
        Number of grid points along the second variable axis. Range: [5, 60]. Default: 29.
    plot_beta: bool
        Whether to plot the safety index (reliability index beta) contours. Default: True.
    plot_alphas: bool
        Whether to plot alpha values (normalized sensitivity factors) for each variable. Default: True.
    plot_base_point: bool
        Whether to plot the base point (mean of input variables) on the diagram. Default: True.
    with_labels: bool
        Whether to add text labels to the base point on the diagram. Default: True.
    ignore_axis_funcs: bool
        Whether to ignore axis transformation functions and plot in original variable space. Default: False.
    view: str | tuple[float, float, float]
        View orientation for 3D perspective. Accepts: 'auto', 'default', 'XY', 'XZ', 'YZ', '-XY', '-XZ', '-YZ' (case-insensitive)
        or tuple (elevation, azimuth, roll) in degrees. Default: 'auto'.
    cmap: str | list
        Colormap specification. Accepts matplotlib colormap name (str) or list of shape (n, 4) with RGBA values in [0, 1].
        Default: 'plasma'.
    type: PlotType
        Plot visualization type (contour / surface). Default: surface.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    n_x_points: int = Field(default=30, ge=5, le=60)
    n_y_points: int = Field(default=29, ge=5, le=60)
    plot_beta: bool = Field(default=True)
    plot_alphas: bool = Field(default=True)
    plot_base_point: bool = Field(default=True)
    with_labels: bool = Field(default=True)
    ignore_axis_funcs: bool = Field(default=False)
    view: str | tuple[float, float, float] = "auto"
    cmap: str | list = "plasma"
    type: PlotType = Field(default=PlotType.surface)

    @field_validator("cmap", mode="after")
    @classmethod
    def check_cmap(cls, v):
        return validate_cmap(v, "RFADplot")

    @field_validator("view", mode="after")
    @classmethod
    def check_view(cls, v):
        return validate_view(v, "RFADplot")


class LSFoptions(BaseModel):
    """
    Options for Limit State Function (LSF) 3D visualization.

    Attributes:
    -----------
    n_x_points: int
        Number of grid points along the first variable axis. Range: [5, 60]. Default: 30.
    n_y_points: int
        Number of grid points along the second variable axis. Range: [5, 60]. Default: 29.
    plot_base_point: bool
        Whether to plot the base point (mean of input variables) on the LSF surface. Default: True.
    plot_failure_point: bool
        Whether to plot the design point (Most Probable Point of Failure) on the LSF surface. Default: True.
    with_labels: bool
        Whether to add text labels to the base and failure points. Default: True.
    ignore_axis_funcs: bool
        Whether to ignore axis transformation functions and plot in original variable space. Default: False.
    view: str | tuple[float, float, float]
        View orientation for 3D perspective. Accepts: 'auto', 'default', 'XY', 'XZ', 'YZ', '-XY', '-XZ', '-YZ' (case-insensitive)
        or tuple (elevation, azimuth, roll) in degrees. Default: 'auto'.
    cmap: str | list
        Colormap specification. Accepts matplotlib colormap name (str) or list of shape (n, 4) with RGBA values in [0, 1].
        Default: 'plasma'.
    type: PlotType
        Plot visualization type (contour / surface). Default: surface.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    n_x_points: int = Field(default=30, ge=5, le=60)
    n_y_points: int = Field(default=29, ge=5, le=60)
    plot_base_point: bool = Field(default=True)
    plot_failure_point: bool = Field(default=True)
    with_labels: bool = Field(default=True)
    ignore_axis_funcs: bool = Field(default=False)
    view: str | tuple[float, float, float] = "auto"
    cmap: str | list = "plasma"
    type: PlotType = Field(default=PlotType.surface)

    @field_validator("cmap", mode="before")
    @classmethod
    def check_cmap(cls, v):
        return validate_cmap(v, "LSFplot")

    @field_validator("view", mode="before")
    @classmethod
    def check_view(cls, v):
        return validate_view(v, "LSFplot")


class ReportingOptions(BaseModel):
    """
    Options for saving analysis results and visualizations.

    Attributes:
    -----------
    save_plots_to_pdf: bool
        Whether to save all generated plots in PDF format. Default: True.
    save_plots_to_pickle: bool
        Whether to save figure objects in pickle format for later retrieval and editing. Default: True.
    save_excel_summary: bool
        Whether to save the numerical results summary to an Excel file. Default: True.
    """

    model_config = ConfigDict(extra="forbid", validate_assignment=True)

    save_plots_to_pdf: bool = Field(default=True)
    save_plots_to_pickle: bool = Field(default=True)
    save_excel_summary: bool = Field(default=True)



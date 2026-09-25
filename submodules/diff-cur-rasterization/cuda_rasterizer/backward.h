#ifndef CUDA_RASTERIZER_BACKWARD_H_INCLUDED
#define CUDA_RASTERIZER_BACKWARD_H_INCLUDED

#include <cuda.h>
#include "cuda_runtime.h"
#include "device_launch_parameters.h"
#define GLM_FORCE_CUDA
#include <glm/glm.hpp>

namespace BACKWARD
{
    void render(
        const dim3 grid, dim3 block,
        const uint2* ranges,
        const uint32_t* point_list,
        int W, int H,
        const float* bg_color,
        const float2* means2D,
        const float4* conic_opacity,
        const float* colors,
        const float* depths,
        const float* view2gaussian,
        const float* all_maps,
        const float* all_map_pixels,
        const float* final_Ts,
        const uint32_t* n_contrib,
        const float* dL_dpixels,
        const float* dL_invdepths,
        const float* dL_dout_all_map,
        const float* dL_dout_distortion,
        float3* dL_dmean2D,
        float4* dL_dconic2D,
        float* dL_dopacity,
        float* dL_dcolors,
        float* dL_dinvdepths,
        float* dL_dall_map,
        const float3* means3D,
        const glm::vec3* scales,
        const glm::vec4* rotations,
        const float* viewmatrix,
        const float scale_modifier,
        float3* dL_dmeans3D,
        const float focal_x, const float focal_y,
        const bool render_geo,
        const bool render_distortion);

    void preprocess(
        int P, int D, int M,
        const float3* means,
        const int* radii,
        const float* shs,
        const bool* clamped,
        const float* opacities,
        const glm::vec3* scales,
        const glm::vec4* rotations,
        const float scale_modifier,
        const float* cov3Ds,
        const float* view,
        const float* proj,
        const float focal_x, float focal_y,
        const float tan_fovx, float tan_fovy,
        const glm::vec3* campos,
        const float3* dL_dmean2D,
        const float* dL_dconics,
        const float* dL_dinvdepth,
        float* dL_dopacity,
        glm::vec3* dL_dmeans,
        float* dL_dcolor,
        float* dL_dcov3D,
        float* dL_dsh,
        glm::vec3* dL_dscale,
        glm::vec4* dL_drot,
        bool antialiasing);
}

#endif

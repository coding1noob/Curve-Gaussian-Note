curve_source="$1"
S="$2"
M="$3"
device="$4"

echo "===== 配置 ====="
echo "曲线先验: $curve_source"
echo "数据集S: $S"
echo "输出目录M: $M"
echo "GPU device: $device"
echo "================="

cd ../gs_pro6000/

unset CUDA_VISIBLE_DEVICES
CUDA_DEVICE_ORDER=PCI_BUS_ID CUDA_VISIBLE_DEVICES="$device" \
python train.py \
-s "$S" \
-m "$M" \
--eval \
--disable_viewer \
--curvegs "$curve_source" \
--curvegs_inject_iteration 3000 \
--edge_non_edge_loss \
--use_outside_Loss \
--outside_dilation_radius 1 \
--outside_alpha_margin 0.0 \
--lambda_outside_rgb 1.0 \
--PGSR_depth \
--multi_view_num 1 \
--multi_view_weight_from_iter 7000 \
--multi_view_weight_end_iter 15000 \
--single_view_weight_from_iter 7000 \
--single_view_weight_end_iter 15000 \
--curve_PGSR

CUDA_DEVICE_ORDER=PCI_BUS_ID \
CUDA_VISIBLE_DEVICES="$device" \
TORCH_HOME=/data1/jhc/torch_cache \
python render_metrics.py \
-s "$S" \
-m "$M" \
--iteration 30000 \
--skip_train

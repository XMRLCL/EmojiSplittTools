"""
表情包分割工具
用于将网格状的表情包图片分割成单独的表情包
"""

import os
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    print("正在安装 Pillow 库...")
    os.system(f"{sys.executable} -m pip install Pillow")
    from PIL import Image

import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class EmojiSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("表情包分割工具")
        self.root.geometry("650x750")
        self.root.resizable(True, True)
        
        self.image_path = None
        self.image = None
        
        self.setup_ui()
    
    def setup_ui(self):
        """设置用户界面"""
        # 主框架
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 标题
        title_label = ttk.Label(main_frame, text="🖼️ 表情包网格分割工具", font=("微软雅黑", 16, "bold"))
        title_label.pack(pady=10)
        
        # 文件选择区域
        file_frame = ttk.LabelFrame(main_frame, text="选择图片", padding="10")
        file_frame.pack(fill=tk.X, pady=5)
        
        self.file_label = ttk.Label(file_frame, text="未选择文件", wraplength=400)
        self.file_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        select_btn = ttk.Button(file_frame, text="浏览...", command=self.select_image)
        select_btn.pack(side=tk.RIGHT, padx=5)
        
        # 图片信息
        self.info_label = ttk.Label(main_frame, text="", font=("微软雅黑", 10))
        self.info_label.pack(pady=5)
        
        # 分割设置区域
        settings_frame = ttk.LabelFrame(main_frame, text="分割设置", padding="10")
        settings_frame.pack(fill=tk.X, pady=10)
        
        # 行数设置
        row_frame = ttk.Frame(settings_frame)
        row_frame.pack(fill=tk.X, pady=5)
        ttk.Label(row_frame, text="行数:", width=10).pack(side=tk.LEFT)
        self.rows_var = tk.StringVar(value="3")
        self.rows_spinbox = ttk.Spinbox(row_frame, from_=1, to=20, textvariable=self.rows_var, width=10)
        self.rows_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 列数设置
        col_frame = ttk.Frame(settings_frame)
        col_frame.pack(fill=tk.X, pady=5)
        ttk.Label(col_frame, text="列数:", width=10).pack(side=tk.LEFT)
        self.cols_var = tk.StringVar(value="3")
        self.cols_spinbox = ttk.Spinbox(col_frame, from_=1, to=20, textvariable=self.cols_var, width=10)
        self.cols_spinbox.pack(side=tk.LEFT, padx=5)
        
        # 自动检测按钮
        auto_frame = ttk.Frame(settings_frame)
        auto_frame.pack(fill=tk.X, pady=5)
        auto_btn = ttk.Button(auto_frame, text="自动检测网格", command=self.auto_detect_grid)
        auto_btn.pack(side=tk.LEFT)
        
        # 预览信息
        self.preview_label = ttk.Label(settings_frame, text="", foreground="blue")
        self.preview_label.pack(pady=5)
        
        # 输出设置
        output_frame = ttk.LabelFrame(main_frame, text="输出设置", padding="10")
        output_frame.pack(fill=tk.X, pady=10)
        
        # 输出文件夹
        out_folder_frame = ttk.Frame(output_frame)
        out_folder_frame.pack(fill=tk.X, pady=5)
        ttk.Label(out_folder_frame, text="输出文件夹:", width=12).pack(side=tk.LEFT)
        self.output_var = tk.StringVar(value="")
        self.output_entry = ttk.Entry(out_folder_frame, textvariable=self.output_var)
        self.output_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        out_browse_btn = ttk.Button(out_folder_frame, text="浏览...", command=self.select_output_folder)
        out_browse_btn.pack(side=tk.RIGHT)
        
        # 文件名前缀
        prefix_frame = ttk.Frame(output_frame)
        prefix_frame.pack(fill=tk.X, pady=5)
        ttk.Label(prefix_frame, text="文件名前缀:", width=12).pack(side=tk.LEFT)
        self.prefix_var = tk.StringVar(value="emoji_")
        self.prefix_entry = ttk.Entry(prefix_frame, textvariable=self.prefix_var, width=20)
        self.prefix_entry.pack(side=tk.LEFT, padx=5)
        
        # 输出格式
        format_frame = ttk.Frame(output_frame)
        format_frame.pack(fill=tk.X, pady=5)
        ttk.Label(format_frame, text="输出格式:", width=12).pack(side=tk.LEFT)
        self.format_var = tk.StringVar(value="PNG")
        format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                     values=["PNG", "JPG", "GIF", "WEBP"], state="readonly", width=10)
        format_combo.pack(side=tk.LEFT, padx=5)
        
        # 分割按钮区域
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(fill=tk.X, pady=20)
        
        # 分割按钮 - 使用更大更明显的样式
        split_btn = tk.Button(btn_frame, text="开始分割", command=self.split_image,
                              font=("微软雅黑", 14, "bold"), bg="#4CAF50", fg="white",
                              width=20, height=2, cursor="hand2")
        split_btn.pack()
        
        # 进度条
        self.progress = ttk.Progressbar(main_frame, mode='determinate')
        self.progress.pack(fill=tk.X, pady=5)
        
        # 状态标签
        self.status_label = ttk.Label(main_frame, text="准备就绪", foreground="gray")
        self.status_label.pack(pady=5)
    
    def select_image(self):
        """选择图片文件"""
        filetypes = [
            ("图片文件", "*.png *.jpg *.jpeg *.gif *.bmp *.webp"),
            ("所有文件", "*.*")
        ]
        path = filedialog.askopenfilename(title="选择表情包图片", filetypes=filetypes)
        if path:
            self.image_path = path
            self.file_label.config(text=os.path.basename(path))
            
            try:
                self.image = Image.open(path)
                width, height = self.image.size
                self.info_label.config(text=f"图片尺寸: {width} x {height} 像素")
                
                # 默认输出到同目录下的子文件夹
                if not self.output_var.get():
                    output_dir = os.path.join(os.path.dirname(path), "分割结果")
                    self.output_var.set(output_dir)
                
                # 使用文件名作为前缀
                base_name = os.path.splitext(os.path.basename(path))[0]
                self.prefix_var.set(f"{base_name}_")
                
                self.update_preview()
            except Exception as e:
                messagebox.showerror("错误", f"无法打开图片: {e}")
    
    def select_output_folder(self):
        """选择输出文件夹"""
        folder = filedialog.askdirectory(title="选择输出文件夹")
        if folder:
            self.output_var.set(folder)
    
    def auto_detect_grid(self):
        """自动检测网格布局 - 通过分析图像边缘和颜色变化"""
        if not self.image:
            messagebox.showwarning("警告", "请先选择图片")
            return
        
        width, height = self.image.size
        
        # 转换为灰度图进行分析
        gray_image = self.image.convert('L')
        pixels = list(gray_image.getdata())
        
        # 方法1: 检测水平和垂直分隔线
        detected_rows, detected_cols = self.detect_grid_lines(gray_image, width, height)
        
        if detected_rows and detected_cols:
            self.rows_var.set(str(detected_rows))
            self.cols_var.set(str(detected_cols))
            cell_w = width // detected_cols
            cell_h = height // detected_rows
            messagebox.showinfo("检测结果", 
                f"检测到网格: {detected_rows}行 x {detected_cols}列\n"
                f"每个表情包约 {cell_w} x {cell_h} 像素")
            self.update_preview()
            return
        
        # 方法2: 基于宽高比推断
        aspect_ratio = width / height
        
        # 常见网格配置
        common_grids = [
            (1, 1), (1, 2), (1, 3), (1, 4),
            (2, 1), (2, 2), (2, 3), (2, 4), (2, 5), (2, 6),
            (3, 1), (3, 2), (3, 3), (3, 4), (3, 5), (3, 6),
            (4, 1), (4, 2), (4, 3), (4, 4), (4, 5),
            (5, 5), (6, 6)
        ]
        
        best_match = None
        best_score = float('inf')
        
        for rows, cols in common_grids:
            # 计算每个单元格的宽高比
            cell_width = width / cols
            cell_height = height / rows
            cell_aspect = cell_width / cell_height
            
            # 假设表情包接近正方形，cell_aspect 应该接近 1
            score = abs(cell_aspect - 1.0)
            
            if score < best_score:
                best_score = score
                best_match = (rows, cols)
        
        if best_match and best_score < 0.3:  # 允许一定的误差
            self.rows_var.set(str(best_match[0]))
            self.cols_var.set(str(best_match[1]))
            cell_w = width // best_match[1]
            cell_h = height // best_match[0]
            messagebox.showinfo("检测结果", 
                f"推测网格: {best_match[0]}行 x {best_match[1]}列\n"
                f"每个表情包约 {cell_w} x {cell_h} 像素\n"
                f"(基于宽高比分析)")
        else:
            # 默认猜测
            if aspect_ratio > 1.3:
                cols = round(aspect_ratio * 2)
                rows = 2
            elif aspect_ratio < 0.7:
                rows = round(2 / aspect_ratio)
                cols = 2
            else:
                rows = 2
                cols = 2
            self.rows_var.set(str(rows))
            self.cols_var.set(str(cols))
            messagebox.showinfo("检测结果", f"建议尝试: {rows}行 x {cols}列")
        
        self.update_preview()
    
    def detect_grid_lines(self, gray_image, width, height):
        """通过检测颜色变化来找到网格分隔线"""
        import numpy as np
        
        try:
            # 转换为numpy数组
            img_array = np.array(gray_image)
            
            # 检测水平分隔线 (行方向的变化)
            row_variance = []
            for y in range(height):
                row = img_array[y, :]
                # 计算这一行的颜色方差
                variance = np.var(row)
                row_variance.append(variance)
            
            # 检测垂直分隔线 (列方向的变化)
            col_variance = []
            for x in range(width):
                col = img_array[:, x]
                variance = np.var(col)
                col_variance.append(variance)
            
            # 找到低方差的区域（可能是分隔线）
            row_var_array = np.array(row_variance)
            col_var_array = np.array(col_variance)
            
            # 检测行数：找到水平方向上的周期性模式
            rows = self.find_grid_count(row_var_array, height)
            cols = self.find_grid_count(col_var_array, width)
            
            return rows, cols
            
        except ImportError:
            return None, None
        except Exception:
            return None, None
    
    def find_grid_count(self, variance_array, total_size):
        """根据方差模式找到网格数量"""
        import numpy as np
        
        # 尝试不同的分割数量
        best_count = None
        best_score = float('inf')
        
        for count in range(1, 10):
            cell_size = total_size / count
            if cell_size < 50:  # 太小的格子不考虑
                continue
            
            # 检查在边界位置的方差是否有规律
            score = 0
            for i in range(1, count):
                boundary = int(i * cell_size)
                # 在边界附近取几个点的平均
                start = max(0, boundary - 3)
                end = min(len(variance_array), boundary + 3)
                local_var = np.mean(variance_array[start:end])
                score += local_var
            
            if count > 1:
                score = score / (count - 1)
                if score < best_score:
                    best_score = score
                    best_count = count
        
        return best_count
    
    def update_preview(self):
        """更新预览信息"""
        if self.image:
            try:
                rows = int(self.rows_var.get())
                cols = int(self.cols_var.get())
                width, height = self.image.size
                cell_width = width // cols
                cell_height = height // rows
                self.preview_label.config(
                    text=f"将生成 {rows * cols} 个表情包，每个尺寸约 {cell_width} x {cell_height} 像素"
                )
            except ValueError:
                pass
    
    def split_image(self):
        """分割图片"""
        if not self.image:
            messagebox.showwarning("警告", "请先选择图片")
            return
        
        try:
            rows = int(self.rows_var.get())
            cols = int(self.cols_var.get())
        except ValueError:
            messagebox.showerror("错误", "请输入有效的行列数")
            return
        
        output_dir = self.output_var.get()
        if not output_dir:
            messagebox.showwarning("警告", "请选择输出文件夹")
            return
        
        # 创建输出目录
        os.makedirs(output_dir, exist_ok=True)
        
        width, height = self.image.size
        cell_width = width // cols
        cell_height = height // rows
        
        prefix = self.prefix_var.get()
        format_ext = self.format_var.get().lower()
        if format_ext == "jpg":
            format_ext = "jpeg"
        
        total = rows * cols
        self.progress['maximum'] = total
        self.progress['value'] = 0
        
        saved_count = 0
        
        try:
            for row in range(rows):
                for col in range(cols):
                    # 计算裁剪区域
                    left = col * cell_width
                    upper = row * cell_height
                    right = left + cell_width
                    lower = upper + cell_height
                    
                    # 裁剪图片
                    cell_image = self.image.crop((left, upper, right, lower))
                    
                    # 生成文件名
                    index = row * cols + col + 1
                    filename = f"{prefix}{index:02d}.{self.format_var.get().lower()}"
                    filepath = os.path.join(output_dir, filename)
                    
                    # 保存图片
                    if self.format_var.get().upper() == "PNG":
                        cell_image.save(filepath, "PNG")
                    elif self.format_var.get().upper() == "JPG":
                        # 如果是RGBA模式，转换为RGB
                        if cell_image.mode == 'RGBA':
                            rgb_image = Image.new('RGB', cell_image.size, (255, 255, 255))
                            rgb_image.paste(cell_image, mask=cell_image.split()[3])
                            rgb_image.save(filepath, "JPEG", quality=95)
                        else:
                            cell_image.save(filepath, "JPEG", quality=95)
                    elif self.format_var.get().upper() == "GIF":
                        cell_image.save(filepath, "GIF")
                    elif self.format_var.get().upper() == "WEBP":
                        cell_image.save(filepath, "WEBP", quality=95)
                    
                    saved_count += 1
                    self.progress['value'] = saved_count
                    self.status_label.config(text=f"正在处理: {saved_count}/{total}")
                    self.root.update()
            
            self.status_label.config(text=f"完成！已保存 {saved_count} 个表情包", foreground="green")
            
            # 询问是否打开输出文件夹
            if messagebox.askyesno("完成", f"成功分割成 {saved_count} 个表情包！\n是否打开输出文件夹？"):
                os.startfile(output_dir)
                
        except Exception as e:
            messagebox.showerror("错误", f"分割失败: {e}")
            self.status_label.config(text="分割失败", foreground="red")


def main():
    root = tk.Tk()
    
    # 设置主题样式
    style = ttk.Style()
    style.theme_use('clam')
    
    app = EmojiSplitterApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()

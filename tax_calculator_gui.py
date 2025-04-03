#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox
from tax_calculator import TaxCalculator, format_money

class TaxCalculatorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("个人所得税计算器2025")
        self.root.geometry("1200x800")  # 增加窗口宽度以适应新布局
        self.calculator = TaxCalculator()
        
        # 设置样式
        style = ttk.Style()
        style.configure("TLabel", padding=5, font=('微软雅黑', 10))
        style.configure("TButton", padding=5, font=('微软雅黑', 10))
        style.configure("TEntry", padding=5, font=('微软雅黑', 10))
        style.configure("Header.TLabel", font=('微软雅黑', 12, 'bold'))
        style.configure("Section.TLabelframe.Label", font=('微软雅黑', 11, 'bold'))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 创建左右分栏
        self.left_frame = ttk.Frame(self.main_frame)
        self.left_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(0, 5))
        
        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S), padx=(5, 0))
        
        # 设置左右分栏的权重
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(1, weight=1)
        
        # 在左侧框架中设置输入部分
        self.setup_income_section()
        self.setup_deduction_section()
        
        # 在右侧框架中设置结果显示部分
        self.setup_result_section()
        
    def setup_income_section(self):
        # 收入部分
        income_frame = ttk.LabelFrame(self.left_frame, text="收入项（请输入）", padding="10", style="Section.TLabelframe")
        income_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 工资薪金
        salary_frame = ttk.Frame(income_frame)
        salary_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(salary_frame, text="工资薪金：").grid(row=0, column=0, sticky=tk.W)
        self.salary_type = tk.StringVar(value="monthly")
        ttk.Radiobutton(salary_frame, text="月收入", variable=self.salary_type, 
                       value="monthly").grid(row=0, column=1)
        ttk.Radiobutton(salary_frame, text="年收入", variable=self.salary_type, 
                       value="annual").grid(row=0, column=2)
        self.salary_entry = ttk.Entry(salary_frame, width=20)
        self.salary_entry.grid(row=0, column=3, padx=5)
        ttk.Label(salary_frame, text="元").grid(row=0, column=4)
        
        # 年终奖
        bonus_frame = ttk.Frame(income_frame)
        bonus_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(bonus_frame, text="年终奖金：").grid(row=0, column=0, sticky=tk.W)
        self.bonus_entry = ttk.Entry(bonus_frame, width=20)
        self.bonus_entry.grid(row=0, column=1, padx=5)
        ttk.Label(bonus_frame, text="元").grid(row=0, column=2)
        self.bonus_type = tk.StringVar(value="separate")
        ttk.Radiobutton(bonus_frame, text="单独计税", variable=self.bonus_type, 
                       value="separate").grid(row=0, column=3)
        ttk.Radiobutton(bonus_frame, text="并入年收入", variable=self.bonus_type, 
                       value="combined").grid(row=0, column=4)
        
        # 其他收入
        other_income_frame = ttk.Frame(income_frame)
        other_income_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # 劳务报酬
        ttk.Label(other_income_frame, text="劳务报酬：").grid(row=0, column=0, sticky=tk.W)
        self.labor_entry = ttk.Entry(other_income_frame, width=20)
        self.labor_entry.grid(row=0, column=1, padx=5)
        ttk.Label(other_income_frame, text="元").grid(row=0, column=2)
        
        # 稿酬
        ttk.Label(other_income_frame, text="稿酬收入：").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.royalty_entry = ttk.Entry(other_income_frame, width=20)
        self.royalty_entry.grid(row=1, column=1, padx=5)
        ttk.Label(other_income_frame, text="元").grid(row=1, column=2)
        
        # 特许权使用费
        ttk.Label(other_income_frame, text="特许权使用费：").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.license_fee_entry = ttk.Entry(other_income_frame, width=20)
        self.license_fee_entry.grid(row=2, column=1, padx=5)
        ttk.Label(other_income_frame, text="元").grid(row=2, column=2)
        
    def setup_deduction_section(self):
        # 专项扣除部分
        deduction_frame = ttk.LabelFrame(self.left_frame, text="专项扣除（请输入）", padding="10", style="Section.TLabelframe")
        deduction_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=10)
        
        # 社保基数
        base_frame = ttk.Frame(deduction_frame)
        base_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(base_frame, text="社保缴纳基数：").grid(row=0, column=0, sticky=tk.W)
        self.insurance_base = ttk.Entry(base_frame, width=15)
        self.insurance_base.grid(row=0, column=1, padx=5)
        ttk.Label(base_frame, text="元/月").grid(row=0, column=2)
        
        # 公积金比例
        ttk.Label(base_frame, text="公积金缴纳比例：").grid(row=0, column=3, sticky=tk.W, padx=(20,0))
        self.housing_fund_ratio = ttk.Entry(base_frame, width=5)
        self.housing_fund_ratio.insert(0, "5")
        self.housing_fund_ratio.grid(row=0, column=4, padx=5)
        ttk.Label(base_frame, text="%").grid(row=0, column=5)
        
        # 三险一金（自动计算）
        insurance_frame = ttk.Frame(deduction_frame)
        insurance_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(insurance_frame, text="养老保险：").grid(row=0, column=0, sticky=tk.W)
        self.pension_entry = ttk.Entry(insurance_frame, width=15, state='readonly')
        self.pension_entry.grid(row=0, column=1, padx=5)
        
        ttk.Label(insurance_frame, text="医疗保险：").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.medical_entry = ttk.Entry(insurance_frame, width=15, state='readonly')
        self.medical_entry.grid(row=0, column=3, padx=5)
        
        ttk.Label(insurance_frame, text="失业保险：").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.unemployment_entry = ttk.Entry(insurance_frame, width=15, state='readonly')
        self.unemployment_entry.grid(row=1, column=1, padx=5)
        
        ttk.Label(insurance_frame, text="住房公积金：").grid(row=1, column=2, sticky=tk.W, padx=(20,0))
        self.housing_fund_entry = ttk.Entry(insurance_frame, width=15, state='readonly')
        self.housing_fund_entry.grid(row=1, column=3, padx=5)
        
        # 绑定基数变化事件
        self.insurance_base.bind('<KeyRelease>', self.update_insurance)
        self.housing_fund_ratio.bind('<KeyRelease>', self.update_insurance)
        
        # 专项附加扣除
        additional_frame = ttk.LabelFrame(self.left_frame, text="专项附加扣除（请输入）", padding="10", style="Section.TLabelframe")
        additional_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=5)
        
        # 子女教育
        ttk.Label(additional_frame, text="子女教育：").grid(row=0, column=0, sticky=tk.W)
        self.children_education = ttk.Entry(additional_frame, width=15)
        self.children_education.grid(row=0, column=1, padx=5)
        
        # 继续教育
        ttk.Label(additional_frame, text="继续教育：").grid(row=0, column=2, sticky=tk.W, padx=(20,0))
        self.continuing_education = ttk.Entry(additional_frame, width=15)
        self.continuing_education.grid(row=0, column=3, padx=5)
        
        # 住房贷款利息
        ttk.Label(additional_frame, text="住房贷款利息：").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.housing_loan = ttk.Entry(additional_frame, width=15)
        self.housing_loan.grid(row=1, column=1, padx=5)
        
        # 住房租金
        ttk.Label(additional_frame, text="住房租金：").grid(row=1, column=2, sticky=tk.W, padx=(20,0))
        self.housing_rent = ttk.Entry(additional_frame, width=15)
        self.housing_rent.grid(row=1, column=3, padx=5)
        
        # 赡养老人
        ttk.Label(additional_frame, text="赡养老人：").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.elderly_care = ttk.Entry(additional_frame, width=15)
        self.elderly_care.grid(row=2, column=1, padx=5)
        
        # 计算按钮移到右边
        button_frame = ttk.Frame(self.left_frame)
        button_frame.grid(row=3, column=0, sticky=(tk.E), pady=20)
        ttk.Button(button_frame, text="计算个人所得税", command=self.calculate_tax, 
                  style="TButton").pack(side=tk.RIGHT, padx=10)
        
    def update_insurance(self, event=None):
        """根据基数和比例更新三险一金金额"""
        try:
            base = float(self.insurance_base.get() or 0)
            ratio = float(self.housing_fund_ratio.get() or 5)
            
            # 限制公积金比例在5-12%之间
            ratio = max(5, min(12, ratio))
            self.housing_fund_ratio.delete(0, tk.END)
            self.housing_fund_ratio.insert(0, str(ratio))
            
            # 计算各项保险金额
            pension = base * 0.08  # 养老保险 8%
            medical = base * 0.02  # 医疗保险 2%
            unemployment = base * 0.005  # 失业保险 0.5%
            housing_fund = base * (ratio / 100)  # 住房公积金
            
            # 更新显示
            self.pension_entry.configure(state='normal')
            self.medical_entry.configure(state='normal')
            self.unemployment_entry.configure(state='normal')
            self.housing_fund_entry.configure(state='normal')
            
            self.pension_entry.delete(0, tk.END)
            self.medical_entry.delete(0, tk.END)
            self.unemployment_entry.delete(0, tk.END)
            self.housing_fund_entry.delete(0, tk.END)
            
            self.pension_entry.insert(0, format_money(pension))
            self.medical_entry.insert(0, format_money(medical))
            self.unemployment_entry.insert(0, format_money(unemployment))
            self.housing_fund_entry.insert(0, format_money(housing_fund))
            
            self.pension_entry.configure(state='readonly')
            self.medical_entry.configure(state='readonly')
            self.unemployment_entry.configure(state='readonly')
            self.housing_fund_entry.configure(state='readonly')
            
        except ValueError:
            pass
            
    def setup_result_section(self):
        # 计算结果显示区域
        result_frame = ttk.LabelFrame(self.right_frame, text="计算结果", padding="10", style="Section.TLabelframe")
        result_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=5)
        
        # 创建文本框和滚动条的容器
        text_container = ttk.Frame(result_frame)
        text_container.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 增加文本框高度和宽度
        self.result_text = tk.Text(text_container, height=30, width=60, font=('微软雅黑', 10))
        self.result_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # 添加滚动条
        scrollbar = ttk.Scrollbar(text_container, orient="vertical", command=self.result_text.yview)
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # 配置文本框的滚动
        self.result_text.configure(yscrollcommand=scrollbar.set)
        
        # 绑定鼠标滚轮事件
        self.result_text.bind('<MouseWheel>', self._on_mousewheel)
        
        # 配置网格权重，使文本框可以随窗口调整大小
        text_container.grid_columnconfigure(0, weight=1)
        text_container.grid_rowconfigure(0, weight=1)
        result_frame.grid_columnconfigure(0, weight=1)
        result_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)
        self.right_frame.grid_rowconfigure(0, weight=1)
        
    def _on_mousewheel(self, event):
        """处理鼠标滚轮事件"""
        self.result_text.yview_scroll(int(-1 * (event.delta / 120)), "units")
        
    def get_deductions_total(self):
        """计算专项扣除和专项附加扣除总额"""
        try:
            # 三险一金
            pension = float(self.pension_entry.get() or 0)
            medical = float(self.medical_entry.get() or 0)
            unemployment = float(self.unemployment_entry.get() or 0)
            housing_fund = float(self.housing_fund_entry.get() or 0)
            
            # 专项附加扣除
            children_edu = float(self.children_education.get() or 0)
            continuing_edu = float(self.continuing_education.get() or 0)
            housing_loan = float(self.housing_loan.get() or 0)
            housing_rent = float(self.housing_rent.get() or 0)
            elderly_care = float(self.elderly_care.get() or 0)
            
            insurance_total = pension + medical + unemployment + housing_fund
            additional_total = (children_edu + continuing_edu + housing_loan + 
                              housing_rent + elderly_care)
            
            return insurance_total, additional_total
            
        except ValueError:
            raise ValueError("请输入有效的数字！")
            
    def calculate_tax(self):
        try:
            # 获取收入数据
            salary = float(self.salary_entry.get() or 0)
            if self.salary_type.get() == "monthly":
                annual_salary = salary * 12
            else:
                annual_salary = salary
                
            bonus = float(self.bonus_entry.get() or 0)
            labor = float(self.labor_entry.get() or 0)
            royalty = float(self.royalty_entry.get() or 0)
            license_fee = float(self.license_fee_entry.get() or 0)
            
            # 获取扣除数据
            insurance_total, additional_total = self.get_deductions_total()
            
            # 计算总收入
            total_income = annual_salary + labor + royalty + license_fee
            if self.bonus_type.get() == "combined":
                total_income += bonus
            
            # 计算应纳税所得额
            taxable_income = total_income - 60000 - insurance_total * 12 - additional_total * 12
            
            # 计算税额
            tax = self.calculator.calculate_accumulated_tax(total_income, 
                                                         60000 + insurance_total * 12 + additional_total * 12, 
                                                         0)
            
            # 如果年终奖单独计税
            bonus_tax = 0
            if bonus > 0 and self.bonus_type.get() == "separate":
                bonus_tax = self.calculator.calculate_bonus_tax(bonus)
            
            # 显示结果
            result = "=== 个人所得税计算结果 ===\n\n"
            result += "【收入项】\n"
            result += f"工资薪金（年）：{format_money(annual_salary)}元\n"
            if bonus > 0:
                result += f"年终奖金：{format_money(bonus)}元 ({self.bonus_type.get() == 'separate' and '单独计税' or '并入年收入'})\n"
            if labor > 0:
                result += f"劳务报酬：{format_money(labor)}元\n"
            if royalty > 0:
                result += f"稿酬收入：{format_money(royalty)}元\n"
            if license_fee > 0:
                result += f"特许权使用费：{format_money(license_fee)}元\n"
            result += f"总收入：{format_money(total_income)}元\n\n"
            
            result += "【费用扣除项】\n"
            result += f"基本减除费用：{format_money(60000)}元\n"
            result += f"三险一金（年）：{format_money(insurance_total * 12)}元\n"
            result += f"专项附加扣除（年）：{format_money(additional_total * 12)}元\n"
            result += f"扣除总额：{format_money(60000 + insurance_total * 12 + additional_total * 12)}元\n\n"
            
            result += "【应纳税额】\n"
            result += f"应纳税所得额：{format_money(taxable_income)}元\n"
            if self.bonus_type.get() == "separate" and bonus > 0:
                result += f"年终奖单独缴税：{format_money(bonus_tax)}元\n"
                result += f"总应缴税额：{format_money(tax + bonus_tax)}元\n"
            else:
                result += f"总应缴税额：{format_money(tax)}元\n"
            
            # 计算并显示年终奖两种方案的对比
            if bonus > 0:
                result += "\n【年终奖方案对比】\n"
                # 单独计税
                separate_bonus_tax = self.calculator.calculate_bonus_tax(bonus)
                separate_total_tax = tax + separate_bonus_tax
                
                # 合并计税
                combined_total_income = total_income + bonus
                combined_tax = self.calculator.calculate_accumulated_tax(
                    combined_total_income,
                    60000 + insurance_total * 12 + additional_total * 12,
                    0
                )
                
                result += f"方案1 - 单独计税：\n"
                result += f"  年终奖税额：{format_money(separate_bonus_tax)}元\n"
                result += f"  总税额：{format_money(separate_total_tax)}元\n\n"
                
                result += f"方案2 - 合并计税：\n"
                result += f"  总税额：{format_money(combined_tax)}元\n\n"
                
                # 计算差额
                tax_diff = abs(combined_tax - separate_total_tax)
                better_plan = "单独计税" if separate_total_tax < combined_tax else "合并计税"
                result += f"税额差额：{format_money(tax_diff)}元\n"
                result += f"建议方案：{better_plan}\n"
            else:
                result += f"总应缴税额：{format_money(tax)}元\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
        except ValueError as e:
            messagebox.showerror("错误", str(e))

def main():
    root = tk.Tk()
    app = TaxCalculatorGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main() 
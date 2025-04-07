document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('taxForm');
    const resultDiv = document.getElementById('result');

    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // 显示加载状态
        resultDiv.innerHTML = '<p class="text-center">计算中...</p>';
        
        // 收集表单数据
        const formData = {
            salary: parseFloat(document.getElementById('salary').value) || 0,
            salary_type: document.getElementById('salary_type').value,
            bonus: parseFloat(document.getElementById('bonus').value) || 0,
            bonus_type: document.getElementById('bonus_type').value,
            labor_income: parseFloat(document.getElementById('labor_income').value) || 0,
            manuscript_income: parseFloat(document.getElementById('manuscript_income').value) || 0,
            license_income: parseFloat(document.getElementById('license_income').value) || 0,
            social_security_base: parseFloat(document.getElementById('social_security_base').value) || 0,
            housing_fund_rate: parseFloat(document.getElementById('housing_fund_rate').value) || 0,
            children_education: parseFloat(document.getElementById('children_education').value) || 0,
            continuing_education: parseFloat(document.getElementById('continuing_education').value) || 0,
            housing_loan: parseFloat(document.getElementById('housing_loan').value) || 0,
            housing_rent: parseFloat(document.getElementById('housing_rent').value) || 0,
            elderly_care: parseFloat(document.getElementById('elderly_care').value) || 0
        };

        try {
            // 发送请求到后端
            const response = await fetch('/calculate', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            });

            const data = await response.json();

            if (data.success) {
                // 显示计算结果
                displayResults(data.result);
            } else {
                // 显示错误信息
                resultDiv.innerHTML = `<div class="error-message">${data.error}</div>`;
            }
        } catch (error) {
            resultDiv.innerHTML = `<div class="error-message">计算过程中发生错误：${error.message}</div>`;
        }
    });

    function displayResults(result) {
        let html = '<div class="result-container">';
        
        // 工资薪金所得
        html += `
            <div class="result-item">
                <h6>工资薪金所得</h6>
                <p>应纳税所得额：¥${result.salary_taxable_income.toFixed(2)}</p>
                <p>应缴税额：¥${result.salary_tax.toFixed(2)}</p>
            </div>
        `;

        // 年终奖金
        if (result.bonus > 0) {
            html += `
                <div class="result-item">
                    <h6>年终奖金</h6>
                    <p>单独计税应纳税所得额：¥${result.bonus_separate_taxable_income.toFixed(2)}</p>
                    <p>单独计税应缴税额：¥${result.bonus_separate_tax.toFixed(2)}</p>
                    <p>合并计税应纳税所得额：¥${result.bonus_combined_taxable_income.toFixed(2)}</p>
                    <p>合并计税应缴税额：¥${result.bonus_combined_tax.toFixed(2)}</p>
                    <p>税额差异：¥${(result.bonus_separate_tax - result.bonus_combined_tax).toFixed(2)}</p>
                    <p class="fw-bold">建议：${result.bonus_recommendation}</p>
                </div>
            `;
        }

        // 劳务报酬
        if (result.labor_income > 0) {
            html += `
                <div class="result-item">
                    <h6>劳务报酬</h6>
                    <p>应纳税所得额：¥${result.labor_taxable_income.toFixed(2)}</p>
                    <p>应缴税额：¥${result.labor_tax.toFixed(2)}</p>
                </div>
            `;
        }

        // 稿酬收入
        if (result.manuscript_income > 0) {
            html += `
                <div class="result-item">
                    <h6>稿酬收入</h6>
                    <p>应纳税所得额：¥${result.manuscript_taxable_income.toFixed(2)}</p>
                    <p>应缴税额：¥${result.manuscript_tax.toFixed(2)}</p>
                </div>
            `;
        }

        // 特许权使用费
        if (result.license_income > 0) {
            html += `
                <div class="result-item">
                    <h6>特许权使用费</h6>
                    <p>应纳税所得额：¥${result.license_taxable_income.toFixed(2)}</p>
                    <p>应缴税额：¥${result.license_tax.toFixed(2)}</p>
                </div>
            `;
        }

        // 总计
        html += `
            <div class="result-item" style="background-color: #e8f4f8;">
                <h6>年终奖金</h6>
                <p>单独计税应纳税所得额：¥${result.bonus_separate_taxable_income.toFixed(2)}</p>
                <p>单独计税应缴税额：¥${result.bonus_separate_tax.toFixed(2)}</p>
                <p>合并计税应纳税所得额：¥${result.bonus_combined_taxable_income.toFixed(2)}</p>
                <p>合并计税应缴税额：¥${result.bonus_combined_tax.toFixed(2)}</p>
                <p>税额差异：¥${(result.bonus_separate_tax - result.bonus_combined_tax).toFixed(2)}</p>
                <p class="fw-bold">建议：${result.bonus_recommendation}</p>
            </div>
        `;

        html += '</div>';
        resultDiv.innerHTML = html;
    }
}); 
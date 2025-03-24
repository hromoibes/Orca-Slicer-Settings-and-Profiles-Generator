// Main JavaScript for Orca Slicer Settings Generator

$(document).ready(function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    const popoverList = popoverTriggerList.map(function (popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });
    
    // Setting explanation functionality
    $('.explain-setting').on('click', function(e) {
        e.preventDefault();
        
        const settingName = $(this).data('setting');
        const settingValue = $(this).data('value');
        const contextData = $(this).data('context') || {};
        const explanationContainer = $($(this).data('target'));
        
        explanationContainer.html('<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>');
        
        // Call API to get explanation
        $.ajax({
            url: '/api/setting/explain',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({
                setting_name: settingName,
                setting_value: settingValue,
                context: contextData
            }),
            success: function(response) {
                let html = '<div class="ai-explanation">';
                html += '<h5><i class="bi bi-lightbulb"></i> AI Explanation</h5>';
                html += '<p>' + response.explanation + '</p>';
                
                if (response.recommendations) {
                    html += '<h6>Recommendations:</h6><ul>';
                    response.recommendations.forEach(function(rec) {
                        html += '<li>' + rec + '</li>';
                    });
                    html += '</ul>';
                }
                
                html += '</div>';
                explanationContainer.html(html);
            },
            error: function() {
                explanationContainer.html('<div class="alert alert-danger">Failed to load explanation. Please try again.</div>');
            }
        });
    });
    
    // Template selection functionality
    $('.template-select').on('change', function() {
        const templateId = $(this).val();
        const templateType = $(this).data('type');
        
        if (!templateId) return;
        
        // Show loading indicator
        $('#template-loading').removeClass('d-none');
        
        // Call API to get template data
        $.ajax({
            url: '/api/' + templateType + '/templates',
            type: 'GET',
            success: function(templates) {
                const template = templates.find(t => t.id === templateId);
                
                if (template) {
                    // Fill form fields with template data
                    Object.keys(template).forEach(function(key) {
                        const input = $('[name="' + key + '"]');
                        if (input.length) {
                            if (input.is(':checkbox')) {
                                input.prop('checked', template[key]);
                            } else {
                                input.val(template[key]);
                            }
                        }
                    });
                    
                    // Special handling for arrays
                    if (template.bed_size && template.bed_size.length === 2) {
                        $('[name="bed_width"]').val(template.bed_size[0]);
                        $('[name="bed_depth"]').val(template.bed_size[1]);
                    }
                    
                    if (template.temp_range_min && template.temp_range_max) {
                        $('[name="temp_min"]').val(template.temp_range_min);
                        $('[name="temp_max"]').val(template.temp_range_max);
                    }
                    
                    if (template.bed_temp_range_min && template.bed_temp_range_max) {
                        $('[name="bed_temp_min"]').val(template.bed_temp_range_min);
                        $('[name="bed_temp_max"]').val(template.bed_temp_range_max);
                    }
                }
                
                // Hide loading indicator
                $('#template-loading').addClass('d-none');
            },
            error: function() {
                // Hide loading indicator
                $('#template-loading').addClass('d-none');
                alert('Failed to load template data. Please try again.');
            }
        });
    });
    
    // Range slider value display
    $('input[type="range"]').on('input', function() {
        const value = $(this).val();
        const displayElement = $($(this).data('display'));
        
        if (displayElement.length) {
            displayElement.text(value);
        }
    });
    
    // Form validation
    $('.needs-validation').on('submit', function(event) {
        if (!this.checkValidity()) {
            event.preventDefault();
            event.stopPropagation();
        }
        
        $(this).addClass('was-validated');
    });
    
    // Confirmation dialogs
    $('.confirm-action').on('click', function(e) {
        if (!confirm($(this).data('confirm-message') || 'Are you sure you want to proceed?')) {
            e.preventDefault();
        }
    });
    
    // Klipper config toggle
    $('.toggle-klipper-config').on('click', function(e) {
        e.preventDefault();
        $($(this).data('target')).toggleClass('d-none');
    });
    
    // Process comparison selection
    $('#compare-select-1, #compare-select-2').on('change', function() {
        const process1 = $('#compare-select-1').val();
        const process2 = $('#compare-select-2').val();
        
        if (process1 && process2 && process1 !== process2) {
            $('#compare-button').prop('disabled', false);
        } else {
            $('#compare-button').prop('disabled', true);
        }
    });
    
    // Material type selection affects temperature ranges
    $('#material-type-select').on('change', function() {
        const materialType = $(this).val();
        
        // Default temperature ranges based on material type
        const tempRanges = {
            'PLA': { min: 190, max: 220, bed_min: 50, bed_max: 60 },
            'PETG': { min: 230, max: 250, bed_min: 70, bed_max: 85 },
            'ABS': { min: 230, max: 250, bed_min: 90, bed_max: 110 },
            'TPU': { min: 220, max: 240, bed_min: 30, bed_max: 50 },
            'Nylon': { min: 240, max: 260, bed_min: 70, bed_max: 90 },
            'PC': { min: 260, max: 280, bed_min: 90, bed_max: 110 }
        };
        
        if (materialType in tempRanges) {
            $('[name="temp_min"]').val(tempRanges[materialType].min);
            $('[name="temp_max"]').val(tempRanges[materialType].max);
            $('[name="bed_temp_min"]').val(tempRanges[materialType].bed_min);
            $('[name="bed_temp_max"]').val(tempRanges[materialType].bed_max);
        }
    });
});

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

def setup_custom_plot(
    ax,
    title='',
    xlabel='',
    ylabel='',
    grid=True,
    xlim=None,
    ylim=None,
    legend=True,
    legend_loc='best',
    major_tick_interval_x=None,
    major_tick_interval_y=None,
    minor_tick=True,
    font_size=12,
    line_width=1.5,
    tick_rotation=0,
    tight_layout=True,
    facecolor='white'
):
    """
    Grafiklerin standart stil ile hazirlanmasi icin kullanilan yardimci fonksiyon.

    Parametreler:
        ax: Plot objesi (plt.gca() veya subplot objesi)
        title: Baslik
        xlabel: X ekseni etiketi
        ylabel: Y ekseni etiketi
        grid: Grid cizgileri gosterilsin mi?
        xlim: X ekseni limiti (tuple)
        ylim: Y ekseni limiti (tuple)
        legend: Lejant gosterilsin mi?
        legend_loc: Lejant konumu
        major_tick_interval_x: X ekseni buyuk tick araligi
        major_tick_interval_y: Y ekseni buyuk tick araligi
        minor_tick: Kucuk tick'ler aktif mi?
        font_size: Etiket ve tick yazilarinin boyutu
        line_width: Grid cizgisi kalinligi
        tick_rotation: X ekseni tick donme acisi
        tight_layout: Layout optimize edilsin mi?
        facecolor: Grafik arka plani rengi
    """

    ax.set_title(title, fontsize=font_size + 2)
    ax.set_xlabel(xlabel, fontsize=font_size)
    ax.set_ylabel(ylabel, fontsize=font_size)

    if xlim:
        ax.set_xlim(xlim)
    if ylim:
        ax.set_ylim(ylim)

    if grid:
        ax.grid(True, which='major', linestyle='--', linewidth=line_width, alpha=0.7)
        if minor_tick:
            ax.minorticks_on()
            ax.grid(True, which='minor', linestyle=':', linewidth=0.8, alpha=0.5)

    ax.tick_params(axis='both', which='major', labelsize=font_size, rotation=tick_rotation)

    if major_tick_interval_x:
        ax.xaxis.set_major_locator(ticker.MultipleLocator(major_tick_interval_x))
    if major_tick_interval_y:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(major_tick_interval_y))

    if legend:
        ax.legend(loc=legend_loc, fontsize=font_size - 1)

    if tight_layout:
        plt.tight_layout()

    ax.set_facecolor(facecolor)

    return ax

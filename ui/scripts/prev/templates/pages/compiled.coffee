module.exports="""
<h1>1. Metrics</h1>
<p>Sagefy uses a larger-than-typical metric system. The rhythm is 24px both vertically and horizontally. The base font size is 16px with a line-height of 24px. Columns are 48px and gutters are 24px. Because of Sagefy&#39;s large metrics, a great deal of focus and minimalism is required.</p>
<p>Different screen sizes alter the number of columns present. While Sagefy is not considered <a href="http://alistapart.com/article/responsive-web-design">responsive web design</a>, it does adjust to available width. Ideas are borrowed from <a href="http://framelessgrid.com/">Frameless Grid</a>, <a href="http://getbootstrap.com/">Twitter Bootstrap</a>, and <a href="http://foundation.zurb.com/">Foundation</a>.</p>



<h2>1.1. Box Sizing</h2>
<p>Sagefy uses the box sizing mode of border box. See the <a href="http://www.paulirish.com/2012/box-sizing-border-box-ftw/">Paul Irish article</a>.</p>



<h2>1.2. Body Layout</h2>
<p>The <code>body</code> element will use up to 20 columns of width in rendering, but will adapt to the user&#39;s available screen real estate.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>body</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><table class="size-table">
    <thead>
        <tr>
            <th>Columns</th>
            <th>Inside</th>
            <th>Outside</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>4</td>
            <td>264px</td>
            <td>312px</td>
        </tr>
        <tr>
            <td>6</td>
            <td>408px</td>
            <td>456px</td>
        </tr>
        <tr>
            <td>8</td>
            <td>552px</td>
            <td>600px</td>
        </tr>
        <tr>
            <td>10</td>
            <td>696px</td>
            <td>744px</td>
        </tr>
        <tr>
            <td>12</td>
            <td>840px</td>
            <td>888px</td>
        </tr>
        <tr>
            <td>14</td>
            <td>984px</td>
            <td>1032px</td>
        </tr>
        <tr>
            <td>16</td>
            <td>1128px</td>
            <td>1176px</td>
        </tr>
        <tr>
            <td>18</td>
            <td>1272px</td>
            <td>1320px</td>
        </tr>
        <tr>
            <td>20</td>
            <td>1416px</td>
            <td>1464px</td>
        </tr>
    </tbody>
</table>
</div><details><summary>Code</summary><pre>&lt;table class=&quot;size-table&quot;&gt;
    &lt;thead&gt;
        &lt;tr&gt;
            &lt;th&gt;Columns&lt;/th&gt;
            &lt;th&gt;Inside&lt;/th&gt;
            &lt;th&gt;Outside&lt;/th&gt;
        &lt;/tr&gt;
    &lt;/thead&gt;
    &lt;tbody&gt;
        &lt;tr&gt;
            &lt;td&gt;4&lt;/td&gt;
            &lt;td&gt;264px&lt;/td&gt;
            &lt;td&gt;312px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;6&lt;/td&gt;
            &lt;td&gt;408px&lt;/td&gt;
            &lt;td&gt;456px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;8&lt;/td&gt;
            &lt;td&gt;552px&lt;/td&gt;
            &lt;td&gt;600px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;10&lt;/td&gt;
            &lt;td&gt;696px&lt;/td&gt;
            &lt;td&gt;744px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;12&lt;/td&gt;
            &lt;td&gt;840px&lt;/td&gt;
            &lt;td&gt;888px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;14&lt;/td&gt;
            &lt;td&gt;984px&lt;/td&gt;
            &lt;td&gt;1032px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;16&lt;/td&gt;
            &lt;td&gt;1128px&lt;/td&gt;
            &lt;td&gt;1176px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;18&lt;/td&gt;
            &lt;td&gt;1272px&lt;/td&gt;
            &lt;td&gt;1320px&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;20&lt;/td&gt;
            &lt;td&gt;1416px&lt;/td&gt;
            &lt;td&gt;1464px&lt;/td&gt;
        &lt;/tr&gt;
    &lt;/tbody&gt;
&lt;/table&gt;
</pre></details>


<h2>1.3. Columns</h2>
<p>Any element may be set to a specific number of columns, using the class <code>col-n</code>. Any element with set columns larger than the available screen will be reduced to the maximum width.</p>
<p>Borrows &quot;magic&quot; from <a href="http://www.helloerik.com/the-subtle-magic-behind-why-the-bootstrap-3-grid-works">Bootstrap&#39;s grid system</a>.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="column-demo row">
    <div class="col-2">col-2</div>
    <div class="col-6">col-6</div>
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;column-demo row&quot;&gt;
    &lt;div class=&quot;col-2&quot;&gt;col-2&lt;/div&gt;
    &lt;div class=&quot;col-6&quot;&gt;col-6&lt;/div&gt;
&lt;/div&gt;
</pre></details>


<h1>2. Global Utilities</h1>
<h2>2.1. Clearfix</h2>
<p>The <code>clearfix</code> class clears any floats within the element so it doesn&#39;t impact neighboring elements.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="clearfix">
    <div class="pull-left push-right">
        Left 1
    </div>
    <div class="pull-left push-right">
        Left 2
    </div>
    <div class="pull-left push-right">
        Left 3
    </div>
    <div class="pull-right">
        Right 3
    </div>
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;clearfix&quot;&gt;
    &lt;div class=&quot;pull-left push-right&quot;&gt;
        Left 1
    &lt;/div&gt;
    &lt;div class=&quot;pull-left push-right&quot;&gt;
        Left 2
    &lt;/div&gt;
    &lt;div class=&quot;pull-left push-right&quot;&gt;
        Left 3
    &lt;/div&gt;
    &lt;div class=&quot;pull-right&quot;&gt;
        Right 3
    &lt;/div&gt;
&lt;/div&gt;
</pre></details>


<h2>2.2. Display Type Helpers</h2>
<p>Helpers that can change the <code>display</code> property on arbitrary elements.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><span class="block">
    A `span` that's now `block`
</span>
<div class="inline-block">
    A `div` that's now `inline-block`
</div>
<div class="inline">
    A `div` that's now `inline`
</div>
</div><details><summary>Code</summary><pre>&lt;span class=&quot;block&quot;&gt;
    A `span` that&#39;s now `block`
&lt;/span&gt;
&lt;div class=&quot;inline-block&quot;&gt;
    A `div` that&#39;s now `inline-block`
&lt;/div&gt;
&lt;div class=&quot;inline&quot;&gt;
    A `div` that&#39;s now `inline`
&lt;/div&gt;
</pre></details>


<h2>2.3. Pull and Push Helpers</h2>
<p>These helpers can apply floating and margins to elements.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="pull-left">
    Pull left
</div>
<div class="pull-right">
    Pull right
</div>
<div class="push-left">
    Push left
</div>
<div class="push-right">
    Push right
</div>
<div class="push-left-gutter">
    Push left gutter
</div>
<div class="push-right-gutter">
    Push right gutter
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;pull-left&quot;&gt;
    Pull left
&lt;/div&gt;
&lt;div class=&quot;pull-right&quot;&gt;
    Pull right
&lt;/div&gt;
&lt;div class=&quot;push-left&quot;&gt;
    Push left
&lt;/div&gt;
&lt;div class=&quot;push-right&quot;&gt;
    Push right
&lt;/div&gt;
&lt;div class=&quot;push-left-gutter&quot;&gt;
    Push left gutter
&lt;/div&gt;
&lt;div class=&quot;push-right-gutter&quot;&gt;
    Push right gutter
&lt;/div&gt;
</pre></details>


<h2>2.4. Vendor Mixins</h2>
<p>Whenever a wrapped property is called, all vendor prefixes are automatically added as well.</p>
<p>The following properties receive vendor mixins:</p>
<ul>
<li>border-radius</li>
<li>transition</li>
<li>box-sizing</li>
<li>filter</li>
<li>flex-flow</li>
<li>justify-content</li>
<li>flex-basis</li>
<li>order</li>
</ul>

<h6 class="sg-field">Parameters</h6>
<ul><li>property</li><li>args</li></ul>
<h6 class="sg-field">Returns</h6>
<ul><li>Styling, for webkit, moz, ms, and o</li></ul>


<h2>2.5. Default Animations</h2>
<p>The primary animation is Sagefy is 200 millisecond linear fade. Animations are limited to transitioning state and representing relationships between elements. User interface animations never exceed 500 milliseconds. Where possible, use CSS for animations over JavaScript.</p>
<p>TODO Give classes, modifiers; show examples</p>



<h1>3. Fonts</h1>
<p>Sagefy uses Palatino for titles and large copy. Sagefy uses Georgia for body copy. Sagefy uses DejaVu Sans Mono derivatives for monospaced.</p>
<ul>
<li><strong>Title</strong>: &quot;palatino linotype&quot;, palatino, palladio, &quot;urw palladio l&quot;, &quot;book antiqua&quot;, serif</li>
<li><strong>Base</strong>: georgia, serif</li>
<li><strong>Monospace</strong>: menlo, &quot;dejavu sans mono&quot;, &quot;bitstream vera sans mono&quot;, consolas, inconsolata, &quot;lucida console&quot;, monaco, monospace</li>
</ul>
<p>The classes <code>title-font</code>, <code>base-font</code> and <code>monospace</code> can be used to alter the typeface.</p>



<h1>4. Colors</h1>
<p>Four primary hues are used by Sagefy. All are generated via <a href="http://www.boronine.com/husl/">huslp</a>.</p>
<ul>
<li><strong>Gold</strong>. 80&deg;, 50% saturation. Serves as the base hue. Also indicates warning.</li>
<li><strong>Blue</strong>. 240&deg;, 100% saturation. Indicates a clickable element or navigation element. Also an accent color when no other is applicable.</li>
<li><strong>Green</strong>. 120&deg;, 100% saturation. Useful for success and acceptance states.</li>
<li><strong>Red</strong>. 0&deg;, 100% saturation. Reserved for errors, danger, major issues, or to provide warmth.</li>
</ul>
<p><strong>Lightness</strong>. Any lightness values may be used. Sagefy recommends against values darker than 20%.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><table class="color-table">
    <thead>
        <tr>
            <th>20%</th>
            <th>40%</th>
            <th>60%</th>
            <th>80%</th>
            <th>90%</th>
            <th>95%</th>
            <th>97%</th>
            <th>99%</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td class="base-color-20"></td>
            <td class="base-color-40"></td>
            <td class="base-color-60"></td>
            <td class="base-color-80"></td>
            <td class="base-color-90"></td>
            <td class="base-color-95"></td>
            <td class="base-color-97"></td>
            <td class="base-color-99"></td>
        </tr>
        <tr>
            <td class="accent-color-20"></td>
            <td class="accent-color-40"></td>
            <td class="accent-color-60"></td>
            <td class="accent-color-80"></td>
            <td class="accent-color-90"></td>
            <td class="accent-color-95"></td>
            <td class="accent-color-97"></td>
            <td class="accent-color-99"></td>
        </tr>
        <tr>
            <td class="good-color-20"></td>
            <td class="good-color-40"></td>
            <td class="good-color-60"></td>
            <td class="good-color-80"></td>
            <td class="good-color-90"></td>
            <td class="good-color-95"></td>
            <td class="good-color-97"></td>
            <td class="good-color-99"></td>
        </tr>
        <tr>
            <td class="bad-color-20"></td>
            <td class="bad-color-40"></td>
            <td class="bad-color-60"></td>
            <td class="bad-color-80"></td>
            <td class="bad-color-90"></td>
            <td class="bad-color-95"></td>
            <td class="bad-color-97"></td>
            <td class="bad-color-99"></td>
        </tr>
    </tbody>
</table>
</div><details><summary>Code</summary><pre>&lt;table class=&quot;color-table&quot;&gt;
    &lt;thead&gt;
        &lt;tr&gt;
            &lt;th&gt;20%&lt;/th&gt;
            &lt;th&gt;40%&lt;/th&gt;
            &lt;th&gt;60%&lt;/th&gt;
            &lt;th&gt;80%&lt;/th&gt;
            &lt;th&gt;90%&lt;/th&gt;
            &lt;th&gt;95%&lt;/th&gt;
            &lt;th&gt;97%&lt;/th&gt;
            &lt;th&gt;99%&lt;/th&gt;
        &lt;/tr&gt;
    &lt;/thead&gt;
    &lt;tbody&gt;
        &lt;tr&gt;
            &lt;td class=&quot;base-color-20&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-40&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-60&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-80&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-90&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-95&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-97&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;base-color-99&quot;&gt;&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td class=&quot;accent-color-20&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-40&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-60&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-80&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-90&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-95&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-97&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;accent-color-99&quot;&gt;&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td class=&quot;good-color-20&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-40&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-60&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-80&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-90&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-95&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-97&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;good-color-99&quot;&gt;&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td class=&quot;bad-color-20&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-40&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-60&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-80&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-90&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-95&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-97&quot;&gt;&lt;/td&gt;
            &lt;td class=&quot;bad-color-99&quot;&gt;&lt;/td&gt;
        &lt;/tr&gt;
    &lt;/tbody&gt;
&lt;/table&gt;
</pre></details>


<h1>5. Links</h1>
<p>Links are simply blue in color, and like other states, <em>lighten</em> on hover and focus, and <em>darken</em> on active (clicked) or selected. Icons can be optionally included in links. Links stay underlined to support the color. Visited links receive no extraordinary treatment.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>a</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>hover</li><li>focus</li><li>active</li><li>selected</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul>
    <li><a href="#">Normal link</a></li>
    <li><a href="#" class="hover">Hovered or focused link</a></li>
    <li><a href="#" class="selected">Active or selected link</a></li>
</ul>
</div><details><summary>Code</summary><pre>&lt;ul&gt;
    &lt;li&gt;&lt;a href=&quot;#&quot;&gt;Normal link&lt;/a&gt;&lt;/li&gt;
    &lt;li&gt;&lt;a href=&quot;#&quot; class=&quot;hover&quot;&gt;Hovered or focused link&lt;/a&gt;&lt;/li&gt;
    &lt;li&gt;&lt;a href=&quot;#&quot; class=&quot;selected&quot;&gt;Active or selected link&lt;/a&gt;&lt;/li&gt;
&lt;/ul&gt;
</pre></details>


<h1>6. Typography</h1>
<p>Sagefy strives to provide basic typographic support for all commonly used HTML5 elements.</p>
<p>For more on excellent web typography, check out <a href="http://practicaltypography.com/">Practical Typography</a>.</p>



<h2>6.1. Font Sizes</h2>
<p>Font sizes are fuzzified by names. Available sizes are:</p>
<ul>
<li>small</li>
<li>normal</li>
<li>accent</li>
<li>large</li>
<li>big</li>
<li>epic</li>
</ul>

<h6 class="sg-field">Example</h6><div class="sg-example"><span class="font-size-small">I'm a huge font size</span>
<span class="font-size-normal">I'm an outstanding font size</span>
<span class="font-size-accent">I'm a small font</span>
<span class="font-size-large">I'm a blend-in font size</span>
<span class="font-size-big">I'm a lovely font size</span>
<span class="font-size-epic">I'm a tiny font size</span>
</div><details><summary>Code</summary><pre>&lt;span class=&quot;font-size-small&quot;&gt;I&#39;m a huge font size&lt;/span&gt;
&lt;span class=&quot;font-size-normal&quot;&gt;I&#39;m an outstanding font size&lt;/span&gt;
&lt;span class=&quot;font-size-accent&quot;&gt;I&#39;m a small font&lt;/span&gt;
&lt;span class=&quot;font-size-large&quot;&gt;I&#39;m a blend-in font size&lt;/span&gt;
&lt;span class=&quot;font-size-big&quot;&gt;I&#39;m a lovely font size&lt;/span&gt;
&lt;span class=&quot;font-size-epic&quot;&gt;I&#39;m a tiny font size&lt;/span&gt;
</pre></details>


<h2>6.2. Width Limiting</h2>
<h2>6.3. Headings, Subheadings, and Header Groups</h2>
<p>All elements <code>h1</code> through <code>h6</code> are styled. Sub-headers use the class <code>subheader</code> when used directly below a higher order header. An <code>hgroup</code> collapses the margins between the headers. Optionally, elements can float along with the header. The most easy way to accomplish this is to wrap the header in an <code>hgroup</code> and add the class <code>inline-block</code> to the header tag.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>h1, h2, h3, h4, h5, h6</li><li>hgroup</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>subheader</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><h1>h1. A Page Level Heading</h1>
<h2>h2. A Section Level Heading</h2>
<h3>h3. A Subsection Level Heading</h3>
<h4>h4. A Division Level Heading</h4>
<h5>h5. Additional Level Heading</h5>
<h6>h6. Small Level Heading</h6>

<hgroup>
    <h1>h1. A Page Level Heading</h1>
    <h2 class="subheader">h2. A subtitle of h1</h2>
    <h3 class="subheader">h3. And a third level title</h3>
</hgroup>

<hgroup>
    <h1 class="inline-block push-right">h1. A Page Level Heading</h1>
    <a href="#"><i class="fa fa-heart"></i>An additional link</a>
</hgroup>
</div><details><summary>Code</summary><pre>&lt;h1&gt;h1. A Page Level Heading&lt;/h1&gt;
&lt;h2&gt;h2. A Section Level Heading&lt;/h2&gt;
&lt;h3&gt;h3. A Subsection Level Heading&lt;/h3&gt;
&lt;h4&gt;h4. A Division Level Heading&lt;/h4&gt;
&lt;h5&gt;h5. Additional Level Heading&lt;/h5&gt;
&lt;h6&gt;h6. Small Level Heading&lt;/h6&gt;

&lt;hgroup&gt;
    &lt;h1&gt;h1. A Page Level Heading&lt;/h1&gt;
    &lt;h2 class=&quot;subheader&quot;&gt;h2. A subtitle of h1&lt;/h2&gt;
    &lt;h3 class=&quot;subheader&quot;&gt;h3. And a third level title&lt;/h3&gt;
&lt;/hgroup&gt;

&lt;hgroup&gt;
    &lt;h1 class=&quot;inline-block push-right&quot;&gt;h1. A Page Level Heading&lt;/h1&gt;
    &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-heart&quot;&gt;&lt;/i&gt;An additional link&lt;/a&gt;
&lt;/hgroup&gt;
</pre></details>


<h2>6.4. Paragraphs</h2>
<p>Paragraphs follow standard conventions. Paragraphs should be no longer than <code>col-10</code>.</p>



<h2>6.5. Leading Paragraphs</h2>
<p>Leading paragraphs, commonly used after the page title, emphasis a block of text. Often leading paragraphs are used to describe the page contents.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>p.leading</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><p class="leading">
    An example paragraph in the leading style.
</p>
</div><details><summary>Code</summary><pre>&lt;p class=&quot;leading&quot;&gt;
    An example paragraph in the leading style.
&lt;/p&gt;
</pre></details>


<h2>6.6. Small, Strong, Emphasis, Deletion, Insertion, Mark, Subscript, Superscript, Abbreviations, and Code</h2>
<p>All normal tag operations are supported and provide expected results. Note that <code>b</code>, <code>s</code>, and <code>u</code> tags are not supported, and <code>i</code> tags are reserved for icons, not italics. Other elements, such as <code>var</code>, <code>samp</code>, and <code>kbd</code>, are styled but non-effectively.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>small, strong, em, del, ins, mark, sub, sub, abbr, code</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul>
    <li><strong>A strong element</strong></li>
    <li><em>An emphasized element</em></li>
    <li><small>A small element</small></li>
    <li><del>A deleted element</del></li>
    <li><ins>An inserted element</ins></li>
    <li><mark>A marked element</mark></li>
    <li><sub>A subscript element</sub> and a normal element</li>
    <li><sup>A superscript element</sup> and a normal element</li>
    <li>An example abbreviation: <abbr data-title="Hypertext Transfer Protocol">HTTP</abbr></li>
    <li><code>Inline code element</code></li>
</ul>
</div><details><summary>Code</summary><pre>&lt;ul&gt;
    &lt;li&gt;&lt;strong&gt;A strong element&lt;/strong&gt;&lt;/li&gt;
    &lt;li&gt;&lt;em&gt;An emphasized element&lt;/em&gt;&lt;/li&gt;
    &lt;li&gt;&lt;small&gt;A small element&lt;/small&gt;&lt;/li&gt;
    &lt;li&gt;&lt;del&gt;A deleted element&lt;/del&gt;&lt;/li&gt;
    &lt;li&gt;&lt;ins&gt;An inserted element&lt;/ins&gt;&lt;/li&gt;
    &lt;li&gt;&lt;mark&gt;A marked element&lt;/mark&gt;&lt;/li&gt;
    &lt;li&gt;&lt;sub&gt;A subscript element&lt;/sub&gt; and a normal element&lt;/li&gt;
    &lt;li&gt;&lt;sup&gt;A superscript element&lt;/sup&gt; and a normal element&lt;/li&gt;
    &lt;li&gt;An example abbreviation: &lt;abbr data-title=&quot;Hypertext Transfer Protocol&quot;&gt;HTTP&lt;/abbr&gt;&lt;/li&gt;
    &lt;li&gt;&lt;code&gt;Inline code element&lt;/code&gt;&lt;/li&gt;
&lt;/ul&gt;
</pre></details>


<h2>6.7. Quotes and Citations</h2>
<p>The <code>q</code> and <code>cite</code> tags are used together to indicate a quote and a citation. All quotes are cited. No quote marks are included when using the <code>q</code> tag. In addition to inline quotations, blockquotes can be used to pull a quote out of inline copy. The <code>q</code> and <code>cite</code> tags are used inside the <code>blockquote</code> tag.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>q, cite, blockquote</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><p>
    <q>Prior knowledge has a large influence on student performance, explaining up to 81 percent of the variance in post-test scores.</q> <cite>Dochy, Segers, and Buehl</cite>
</p>

<blockquote>
    <q>Prior knowledge has a large influence on student performance, explaining up to 81 percent of the variance in post-test scores.</q>
    <cite>Dochy, Segers, and Buehl</cite>
</blockquote>
</div><details><summary>Code</summary><pre>&lt;p&gt;
    &lt;q&gt;Prior knowledge has a large influence on student performance, explaining up to 81 percent of the variance in post-test scores.&lt;/q&gt; &lt;cite&gt;Dochy, Segers, and Buehl&lt;/cite&gt;
&lt;/p&gt;

&lt;blockquote&gt;
    &lt;q&gt;Prior knowledge has a large influence on student performance, explaining up to 81 percent of the variance in post-test scores.&lt;/q&gt;
    &lt;cite&gt;Dochy, Segers, and Buehl&lt;/cite&gt;
&lt;/blockquote&gt;
</pre></details>


<h2>6.8. Horizontal Rules</h2>
<p>Horizontal rules are avoided as Sagefy prefers whitespace over lines. Rules are useful in certain situations, however.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>hr</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><hr />
</div><details><summary>Code</summary><pre>&lt;hr /&gt;
</pre></details>


<h2>6.9. Definition</h2>
<p>The <code>dfn</code> element can be used on the defining instance of a term. It is often used with a title attribute with a defintion of the term.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>dfn</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example">An example definition of <dfn data-title="The perception of fluctuations of air pressure.">sound</dfn>.
</div><details><summary>Code</summary><pre>An example definition of &lt;dfn data-title=&quot;The perception of fluctuations of air pressure.&quot;&gt;sound&lt;/dfn&gt;.
</pre></details>


<h2>6.10. Time and Dates</h2>
<p>The <code>time</code> tag is used to describe specific dates and times. It does not indicate durations. The <code>datetime</code> attribute is optional.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>time</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><time datetime="2009-11-13">November 13<sup>th</sup></time>
</div><details><summary>Code</summary><pre>&lt;time datetime=&quot;2009-11-13&quot;&gt;November 13&lt;sup&gt;th&lt;/sup&gt;&lt;/time&gt;
</pre></details>


<h2>6.11. Addresses, Header, Footer, Aside, Section, Article, Nav</h2>
<p>Addresses are commonly misunderstood elements. The <code>address</code> tag is used to indicate who to contact for a particular document. The tag is not used for arbitrary postal addresses and email address. Sagefy does not style the <code>address</code> tag. Other block tags such as header and footer are used for semantic representation, but receive no special styling.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>address, header, footer, aside, section, article, nav</li></ul>


<h2>6.12. Programming Code and Preformatted Elements</h2>
<p>Preformatted element defaults to use monospaced fonts. Computer code is syntax highlighted based on language.</p>
<ul>
<li><a href="http://highlightjs.org/">Highlight.js</a></li>
</ul>

<h6 class="sg-field">Elements</h6>
<ul><li>pre</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><pre> $ ->
    $anchor = $ 'a[href*="\\"]'
    $anchor.click ->
        $(this).attr "target", "_blank"
        true
</pre>
</div><details><summary>Code</summary><pre>&lt;pre&gt; $ -&gt;
    $anchor = $ &#39;a[href*=&quot;\\&quot;]&#39;
    $anchor.click -&gt;
        $(this).attr &quot;target&quot;, &quot;_blank&quot;
        true
&lt;/pre&gt;
</pre></details>


<h1>7. Images</h1>
<p>Alt tags, title tags, and captions for images are recommended where possible. Images subscribe to the basic grid of <code>12px</code> as much as possible, more so on the width. Additionally, widths that match the grid system, <code>48n + 24(n-1)</code>, are preferable.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>img</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><img src="https://placekitten.com/g/24/24" /> <img src="https://placekitten.com/g/48/48" /> <img src="https://placekitten.com/g/60/60" /> <img src="https://placekitten.com/g/72/72" /> <img src="https://placekitten.com/g/96/96" /> <img src="https://placekitten.com/g/120/120" /></div><details><summary>Code</summary><pre>&lt;img src=&quot;https://placekitten.com/g/24/24&quot; /&gt; &lt;img src=&quot;https://placekitten.com/g/48/48&quot; /&gt; &lt;img src=&quot;https://placekitten.com/g/60/60&quot; /&gt; &lt;img src=&quot;https://placekitten.com/g/72/72&quot; /&gt; &lt;img src=&quot;https://placekitten.com/g/96/96&quot; /&gt; &lt;img src=&quot;https://placekitten.com/g/120/120&quot; /&gt;</pre></details>


<h2>7.1. Icons</h2>
<p>Sagefy uses <a href="https://fortawesome.github.io/Font-Awesome/">FontAwesome</a> where applicable. Use the <code>i</code> tag for icons, not italics. When presenting icons, label the icon. If you must choose between an icon and text, prefer text.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>i</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>Many, see the list <a href="https://fortawesome.github.io/Font-Awesome/icons/">here</a></li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul class="inline"> <li><i class="fa fa-compass"></i></li> <li><i class="fa fa-quote-right"></i></li> <li><i class="fa fa-hand-o-left"></i></li> <li><i class="fa fa-rocket"></i></li> <li><i class="fa fa-search"></i></li> <li><i class="fa fa-refresh"></i></li> <li><i class="fa fa-group"></i></li> </ul></div><details><summary>Code</summary><pre>&lt;ul class=&quot;inline&quot;&gt; &lt;li&gt;&lt;i class=&quot;fa fa-compass&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;li&gt;&lt;i class=&quot;fa fa-quote-right&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;li&gt;&lt;i class=&quot;fa fa-hand-o-left&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;li&gt;&lt;i class=&quot;fa fa-rocket&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;li&gt;&lt;i class=&quot;fa fa-search&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;li&gt;&lt;i class=&quot;fa fa-refresh&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;li&gt;&lt;i class=&quot;fa fa-group&quot;&gt;&lt;/i&gt;&lt;/li&gt; &lt;/ul&gt;</pre></details>


<h2>7.2. Image Captions</h2>
<p>Images can be framed by wrapping them in a <code>figure</code> tag. Be sure to subtract 20px to account for padding incurred. The <code>figcaption</code> tag can be used inside of a <code>figure</code> tag to add a caption. This prodecure is useful but not limited to images.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>figure</li><li>figcaption</li><li>img</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><figure> <img src="https://placekitten.com/g/120/120" /> <figcaption>Figcaptions are not limited to images, but images are an excellent example.</figcaption> </figure></div><details><summary>Code</summary><pre>&lt;figure&gt; &lt;img src=&quot;https://placekitten.com/g/120/120&quot; /&gt; &lt;figcaption&gt;Figcaptions are not limited to images, but images are an excellent example.&lt;/figcaption&gt; &lt;/figure&gt;</pre></details>


<h2>7.3. Avatars</h2>
<p>Avatars simply use the <a href="https://en.gravatar.com/">Gravatar</a> system. Sizes match the image sizes stated above. Avatars are not captioned.</p>
<p>TODO Add avatar example</p>



<h2>7.4. Logos and Branding</h2>
<p>The Sagefy logo is a mariner&#39;s astrolabe. It is presented on all pages, and clicking it either returns to a home page or presents an overlayed menu of options. The Sagefy name, when used independently or with the logo, is lowercase, normal weight Palatino in color <code>#343115</code>. It is not required to accompany the logo. When used in a sentence or title, Sagefy is capitalized.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><img src="/astrolabe.svg" height="300" /></div><details><summary>Code</summary><pre>&lt;img src=&quot;/astrolabe.svg&quot; height=&quot;300&quot; /&gt;</pre></details>


<h2>7.5. Region Flags</h2>
<p>Where applicable, we use <a href="https://github.com/koppi/iso-country-flags-svg-collection">this collection</a> of flags for countries and regions.</p>
<p>TODO Add Region Flags example</p>



<h1>8. Lists</h1>
<p>Unordered lists follow standard conventions. Line items do not hold extra margins. Only root-level unordered lists have a bottom margin. Ordered lists follow the standard conventions as well.</p>
<p>Lists can be unstyled using the <code>unstyled</code> class. Margins still count on lower level lists.</p>
<p>Horizontal, or inline, lists are also supported. Often used as simple navigational menus. Subitems do not appear.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>ul, ol, li</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>unstyled</li><li>horizontal</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul>
    <li>Item 1
        <ul>
            <li>Item 1.1</li>
            <li>Item 1.2</li>
            <li>Item 1.3</li>
        </ul>
    </li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>

<ol>
    <li>Item 1
        <ul>
            <li>Item 1.1</li>
            <li>Item 1.2</li>
            <li>Item 1.3</li>
        </ul>
    </li>
    <li>Item 2</li>
    <li>Item 3</li>
</ol>

<ul class="unstyled">
    <li>Item 1
        <ul>
            <li>Item 1.1</li>
            <li>Item 1.2</li>
            <li>Item 1.3</li>
        </ul>
    </li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>

<ul class="horizontal">
    <li>Item 1</li>
    <li>Item 2</li>
    <li>Item 3</li>
</ul>
</div><details><summary>Code</summary><pre>&lt;ul&gt;
    &lt;li&gt;Item 1
        &lt;ul&gt;
            &lt;li&gt;Item 1.1&lt;/li&gt;
            &lt;li&gt;Item 1.2&lt;/li&gt;
            &lt;li&gt;Item 1.3&lt;/li&gt;
        &lt;/ul&gt;
    &lt;/li&gt;
    &lt;li&gt;Item 2&lt;/li&gt;
    &lt;li&gt;Item 3&lt;/li&gt;
&lt;/ul&gt;

&lt;ol&gt;
    &lt;li&gt;Item 1
        &lt;ul&gt;
            &lt;li&gt;Item 1.1&lt;/li&gt;
            &lt;li&gt;Item 1.2&lt;/li&gt;
            &lt;li&gt;Item 1.3&lt;/li&gt;
        &lt;/ul&gt;
    &lt;/li&gt;
    &lt;li&gt;Item 2&lt;/li&gt;
    &lt;li&gt;Item 3&lt;/li&gt;
&lt;/ol&gt;

&lt;ul class=&quot;unstyled&quot;&gt;
    &lt;li&gt;Item 1
        &lt;ul&gt;
            &lt;li&gt;Item 1.1&lt;/li&gt;
            &lt;li&gt;Item 1.2&lt;/li&gt;
            &lt;li&gt;Item 1.3&lt;/li&gt;
        &lt;/ul&gt;
    &lt;/li&gt;
    &lt;li&gt;Item 2&lt;/li&gt;
    &lt;li&gt;Item 3&lt;/li&gt;
&lt;/ul&gt;

&lt;ul class=&quot;horizontal&quot;&gt;
    &lt;li&gt;Item 1&lt;/li&gt;
    &lt;li&gt;Item 2&lt;/li&gt;
    &lt;li&gt;Item 3&lt;/li&gt;
&lt;/ul&gt;
</pre></details>


<h2>8.1. Lists with Thumbnails</h2>
<p>A very common on the internet is a list featuring thumbnails. These lists are zebra-striped and can be marked up either as actual lists, or for convienence, tables. Lists with thumbnails use the <code>with-thumbnails</code> class.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>table, tr...</li><li>ul, li...</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>with-thumbnails</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><table class="list--with-thumbnails">
    <tr>
        <td>
            <img src="https://placekitten.com/g/40/40" data-title="40x40" />
        </td>
        <td>
            <h4>List Item 1</h4>
            <p>A description of list item 1.</p>
        </td>
    </tr>
    <tr>
        <td>
            <img src="https://placekitten.com/g/40/40" data-title="40x40" />
        </td>
        <td>
            <h4>List Item 1</h4>
            <p>A description of list item 1.</p>
        </td>
    </tr>
    <tr>
        <td>
            <img src="https://placekitten.com/g/40/40" data-title="40x40" />
        </td>
        <td>
            <h4>List Item 1</h4>
            <p>A description of list item 1.</p>
        </td>
    </tr>
</table>
</div><details><summary>Code</summary><pre>&lt;table class=&quot;list--with-thumbnails&quot;&gt;
    &lt;tr&gt;
        &lt;td&gt;
            &lt;img src=&quot;https://placekitten.com/g/40/40&quot; data-title=&quot;40x40&quot; /&gt;
        &lt;/td&gt;
        &lt;td&gt;
            &lt;h4&gt;List Item 1&lt;/h4&gt;
            &lt;p&gt;A description of list item 1.&lt;/p&gt;
        &lt;/td&gt;
    &lt;/tr&gt;
    &lt;tr&gt;
        &lt;td&gt;
            &lt;img src=&quot;https://placekitten.com/g/40/40&quot; data-title=&quot;40x40&quot; /&gt;
        &lt;/td&gt;
        &lt;td&gt;
            &lt;h4&gt;List Item 1&lt;/h4&gt;
            &lt;p&gt;A description of list item 1.&lt;/p&gt;
        &lt;/td&gt;
    &lt;/tr&gt;
    &lt;tr&gt;
        &lt;td&gt;
            &lt;img src=&quot;https://placekitten.com/g/40/40&quot; data-title=&quot;40x40&quot; /&gt;
        &lt;/td&gt;
        &lt;td&gt;
            &lt;h4&gt;List Item 1&lt;/h4&gt;
            &lt;p&gt;A description of list item 1.&lt;/p&gt;
        &lt;/td&gt;
    &lt;/tr&gt;
&lt;/table&gt;
</pre></details>


<h2>8.2. Definition Lists</h2>
<p>Definition lists are useful for glossaries, dictionaries, and outlines. The tags <code>dl</code>, <code>dt</code>, and <code>dd</code> are used together to form the definition list. Definition lists are also used for marking up metadata.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>dl, dt, dd</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><dl>
    <dt>RSS</dt>
    <dd>An XML format for aggregating information from websites whose
    content is frequently updated.</dd>
    <dt>Weblog</dt>
    <dd>Contraction of the term "web log", a weblog is a
    website that is periodically updated, like a journal</dd>
</dl>
</div><details><summary>Code</summary><pre>&lt;dl&gt;
    &lt;dt&gt;RSS&lt;/dt&gt;
    &lt;dd&gt;An XML format for aggregating information from websites whose
    content is frequently updated.&lt;/dd&gt;
    &lt;dt&gt;Weblog&lt;/dt&gt;
    &lt;dd&gt;Contraction of the term &quot;web log&quot;, a weblog is a
    website that is periodically updated, like a journal&lt;/dd&gt;
&lt;/dl&gt;
</pre></details>


<h1>9. Forms</h1>
<p>Forms are perhaps the most complicated part of any web design. The Sagefy style guide provides a usable, consistent, comprehensive approach to form elements. Forms typically have only a single column of fields. Most forms terminate with one, and only one, primary action button and several possible secondary actions. Most standard forms start with a title and short description of the form.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <h3>
        A basic form
    </h3>
    <div class="form-description">
        A description of a basic form.
    </div>
    <div class="form-field form-field--text">
        <label for="name">Name</label>
        <input id="name" name="name" placeholder="e.g. Marissa" size="50" type="text" />
        <p class="form-field__description">
            Your name belongs in the box
        </p>
    </div>
    <div class="form-field form-field--boolean">
        <label for="spam">
            <input name="spam" id="spam" type="checkbox" value="y">
            Send me spam
        </label>
    </div>
    <div class="form-field form-field--textarea">
        <label for="thoughts">My thoughts on spam</label>
        <textarea cols="40" id="thoughts" name="thoughts" rows="4"></textarea>
    </div>
    <button type="submit">
        <i class="fa fa-check"></i>
        Send
    </button>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;h3&gt;
        A basic form
    &lt;/h3&gt;
    &lt;div class=&quot;form-description&quot;&gt;
        A description of a basic form.
    &lt;/div&gt;
    &lt;div class=&quot;form-field form-field--text&quot;&gt;
        &lt;label for=&quot;name&quot;&gt;Name&lt;/label&gt;
        &lt;input id=&quot;name&quot; name=&quot;name&quot; placeholder=&quot;e.g. Marissa&quot; size=&quot;50&quot; type=&quot;text&quot; /&gt;
        &lt;p class=&quot;form-field__description&quot;&gt;
            Your name belongs in the box
        &lt;/p&gt;
    &lt;/div&gt;
    &lt;div class=&quot;form-field form-field--boolean&quot;&gt;
        &lt;label for=&quot;spam&quot;&gt;
            &lt;input name=&quot;spam&quot; id=&quot;spam&quot; type=&quot;checkbox&quot; value=&quot;y&quot;&gt;
            Send me spam
        &lt;/label&gt;
    &lt;/div&gt;
    &lt;div class=&quot;form-field form-field--textarea&quot;&gt;
        &lt;label for=&quot;thoughts&quot;&gt;My thoughts on spam&lt;/label&gt;
        &lt;textarea cols=&quot;40&quot; id=&quot;thoughts&quot; name=&quot;thoughts&quot; rows=&quot;4&quot;&gt;&lt;/textarea&gt;
    &lt;/div&gt;
    &lt;button type=&quot;submit&quot;&gt;
        &lt;i class=&quot;fa fa-check&quot;&gt;&lt;/i&gt;
        Send
    &lt;/button&gt;
&lt;/form&gt;
</pre></details>


<h2>9.1. Form Description</h2>
<p>A form may need an explanation as to why the data is required from the user.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>.form-description</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <h3>
        A basic form
    </h3>
    <div class="form-description">
        A description of a basic form.
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;h3&gt;
        A basic form
    &lt;/h3&gt;
    &lt;div class=&quot;form-description&quot;&gt;
        A description of a basic form.
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h2>9.2. Fieldsets and Legends</h2>
<p>Many users have difficult with forms with more than three fields. In such situations, it is useful to group the fields into fieldsets and legends to segment the field. These fieldsets can also be constructed as a step-by-step wizard.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>fieldset, legend</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text">
        <label for="name">Name</label>
        <input id="name" name="name" placeholder="e.g. Marissa" size="50" type="text" />
        <p class="form-field__description">
            Your name belongs in the box
        </p>
    </div>
    <fieldset>
        <legend>Spam Fields</legend>
        <div class="form-field form-field--boolean">
            <label for="spam">
                <input name="spam" id="spam" type="checkbox" value="y">
                Send me spam
            </label>
        </div>
        <div class="form-field form-field--textarea">
            <label for="thoughts">My thoughts on spam</label>
            <textarea cols="40" id="thoughts" name="thoughts" rows="4"></textarea>
        </div>
    </fieldset>
    <button type="submit">
        <i class="fa fa-check"></i>
        Send
    </button>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text&quot;&gt;
        &lt;label for=&quot;name&quot;&gt;Name&lt;/label&gt;
        &lt;input id=&quot;name&quot; name=&quot;name&quot; placeholder=&quot;e.g. Marissa&quot; size=&quot;50&quot; type=&quot;text&quot; /&gt;
        &lt;p class=&quot;form-field__description&quot;&gt;
            Your name belongs in the box
        &lt;/p&gt;
    &lt;/div&gt;
    &lt;fieldset&gt;
        &lt;legend&gt;Spam Fields&lt;/legend&gt;
        &lt;div class=&quot;form-field form-field--boolean&quot;&gt;
            &lt;label for=&quot;spam&quot;&gt;
                &lt;input name=&quot;spam&quot; id=&quot;spam&quot; type=&quot;checkbox&quot; value=&quot;y&quot;&gt;
                Send me spam
            &lt;/label&gt;
        &lt;/div&gt;
        &lt;div class=&quot;form-field form-field--textarea&quot;&gt;
            &lt;label for=&quot;thoughts&quot;&gt;My thoughts on spam&lt;/label&gt;
            &lt;textarea cols=&quot;40&quot; id=&quot;thoughts&quot; name=&quot;thoughts&quot; rows=&quot;4&quot;&gt;&lt;/textarea&gt;
        &lt;/div&gt;
    &lt;/fieldset&gt;
    &lt;button type=&quot;submit&quot;&gt;
        &lt;i class=&quot;fa fa-check&quot;&gt;&lt;/i&gt;
        Send
    &lt;/button&gt;
&lt;/form&gt;
</pre></details>


<h2>9.3. Form Fields</h2>
<p>Form fields are wrapped in a class of <code>form-field</code> and the type of the form field, such as <code>form-field--text</code>.</p>



<h3>9.3.1. Field Labels</h3>
<p>Every field that is not in a horizontal form has a label. The label clicks to focus on the related form element. Forms typically have labels above the field.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>label</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text">
        <label for="name">Name</label>
        <input id="name" name="name" placeholder="e.g. Marissa" size="50" type="text" />
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text&quot;&gt;
        &lt;label for=&quot;name&quot;&gt;Name&lt;/label&gt;
        &lt;input id=&quot;name&quot; name=&quot;name&quot; placeholder=&quot;e.g. Marissa&quot; size=&quot;50&quot; type=&quot;text&quot; /&gt;
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h3>9.3.2. Field Descriptions</h3>
<p>In the standard vertical layout, each form field may have a short description below the field. These descriptions are particularly useful when the user may not understand the expected input, or has reservations about why the field is necessary or beneficial. Fields typically have descriptions below the field.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text">
        <label for="name">Name</label>
        <input id="name" name="name" placeholder="e.g. Marissa" size="50" type="text" />
        <p class="form-field__description">
            We need a name to identify you to other users.
        </p>
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text&quot;&gt;
        &lt;label for=&quot;name&quot;&gt;Name&lt;/label&gt;
        &lt;input id=&quot;name&quot; name=&quot;name&quot; placeholder=&quot;e.g. Marissa&quot; size=&quot;50&quot; type=&quot;text&quot; /&gt;
        &lt;p class=&quot;form-field__description&quot;&gt;
            We need a name to identify you to other users.
        &lt;/p&gt;
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h3>9.3.3. Optional and Required Fields</h3>
<p>The label may contain a <code>span</code> with either <code>optional</code> or <code>required</code> as the class and copy to indicate the field is either required or optional. More useful for forms with more than three fields or several sections.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>.required</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text">
        <label for="name">Name <span class="required">required</span></label>
        <input id="name" name="name" placeholder="e.g. Marissa" size="50" type="text" />
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text&quot;&gt;
        &lt;label for=&quot;name&quot;&gt;Name &lt;span class=&quot;required&quot;&gt;required&lt;/span&gt;&lt;/label&gt;
        &lt;input id=&quot;name&quot; name=&quot;name&quot; placeholder=&quot;e.g. Marissa&quot; size=&quot;50&quot; type=&quot;text&quot; /&gt;
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h3>9.3.4. Form Feedback</h3>
<p>Forms typically have validation messages to the right of the field.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>form-field__feedback</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>--success</li><li>--error</li><li>--warning</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text form-field--success">
        <label>Success</label>
        <input type="text" placeholder="Example success" />
        <span class="form-field__feedback">
            <i class="fa fa-check"></i>
            This is a success
        </span>
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text form-field--success&quot;&gt;
        &lt;label&gt;Success&lt;/label&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example success&quot; /&gt;
        &lt;span class=&quot;form-field__feedback&quot;&gt;
            &lt;i class=&quot;fa fa-check&quot;&gt;&lt;/i&gt;
            This is a success
        &lt;/span&gt;
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h3>9.3.5. Disabled Form Fields</h3>
<p>Disabling for elements causes them to lose opacity.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>input, textarea, select</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>disabled</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text form-field--disabled">
        <label>Disabled</label>
        <input type="text" placeholder="Example disabled" disabled="disabled" />
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text form-field--disabled&quot;&gt;
        &lt;label&gt;Disabled&lt;/label&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example disabled&quot; disabled=&quot;disabled&quot; /&gt;
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h3>9.3.6. Buttons</h3>
<p>Buttons are one of the most recognized elements of web design. Sagefy provides buttons in a variety of styles. The modifiers are based on role, not appearance. In most places, where there are multiple buttons, one and only one button should be emphasized.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>button</li><li>a.button</li><li>.button-group (wrapper)</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>Roles - primary - secondary - danger - cancel</li><li>disabled</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul class="unstyled">
    <li>
        <button class="button--primary">
            Primary
        </button>

        Navigation, Next
    </li>
    <li>
        <button class="button--secondary">
            Secondary
        </button>

        Success, Accept
    </li>
    <li>
        <button class="button--danger">
            Danger
        </button>

        Error, Delete
    </li>
    <li>
        <button class="button--cancel">
            Cancel
        </button>

        Escape, Previous, Back, Information
    </li>
</ul>

<ul class="inline">
    <li>
        <button class="button--primary">
            Next Page
            <i class="fa fa-chevron-right"></i>
        </button>
    </li>
    <li>
        <button class="button--secondary">
            <i class="fa fa-edit"></i>
            Edit
        </button>
    </li>
    <li>
        <button class="button--danger">
            <i class="fa fa-trash-o"></i>
            Delete
        </button>
    </li>
    <li>
        <button class="button--cancel">
            <i class="fa fa-refresh"></i>
            Resume
        </button>
    </li>
</ul>

<div></div>

<ul class="inline">
    <li>
        <button class="button--primary" disabled>
            Next Page
            <i class="fa fa-chevron-right"></i>
        </button>
    </li>
    <li>
        <button class="button--secondary" disabled>
            <i class="fa fa-edit"></i>
            Edit
        </button>
    </li>
    <li>
        <button class="button--danger" disabled>
            <i class="fa fa-trash-o"></i>
            Delete
        </button>
    </li>
    <li>
        <button class="button--cancel" disabled>
            <i class="fa fa-refresh"></i>
            Resume
        </button>
    </li>
</ul>

<div class="button-group">
    <button class="button--primary">
        Next Page
        <i class="fa fa-chevron-right"></i>
    </button>
    <button class="button--secondary">
        <i class="fa fa-edit"></i>
        Edit
    </button>
    <button class="button--danger">
        <i class="fa fa-trash-o"></i>
        Delete
    </button>
    <button class="button--cancel">
        <i class="fa fa-refresh"></i>
        Resume
    </button>
</div>
</div><details><summary>Code</summary><pre>&lt;ul class=&quot;unstyled&quot;&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--primary&quot;&gt;
            Primary
        &lt;/button&gt;

        Navigation, Next
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--secondary&quot;&gt;
            Secondary
        &lt;/button&gt;

        Success, Accept
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--danger&quot;&gt;
            Danger
        &lt;/button&gt;

        Error, Delete
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--cancel&quot;&gt;
            Cancel
        &lt;/button&gt;

        Escape, Previous, Back, Information
    &lt;/li&gt;
&lt;/ul&gt;

&lt;ul class=&quot;inline&quot;&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--primary&quot;&gt;
            Next Page
            &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
        &lt;/button&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--secondary&quot;&gt;
            &lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt;
            Edit
        &lt;/button&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--danger&quot;&gt;
            &lt;i class=&quot;fa fa-trash-o&quot;&gt;&lt;/i&gt;
            Delete
        &lt;/button&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--cancel&quot;&gt;
            &lt;i class=&quot;fa fa-refresh&quot;&gt;&lt;/i&gt;
            Resume
        &lt;/button&gt;
    &lt;/li&gt;
&lt;/ul&gt;

&lt;div&gt;&lt;/div&gt;

&lt;ul class=&quot;inline&quot;&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--primary&quot; disabled&gt;
            Next Page
            &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
        &lt;/button&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--secondary&quot; disabled&gt;
            &lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt;
            Edit
        &lt;/button&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--danger&quot; disabled&gt;
            &lt;i class=&quot;fa fa-trash-o&quot;&gt;&lt;/i&gt;
            Delete
        &lt;/button&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;button class=&quot;button--cancel&quot; disabled&gt;
            &lt;i class=&quot;fa fa-refresh&quot;&gt;&lt;/i&gt;
            Resume
        &lt;/button&gt;
    &lt;/li&gt;
&lt;/ul&gt;

&lt;div class=&quot;button-group&quot;&gt;
    &lt;button class=&quot;button--primary&quot;&gt;
        Next Page
        &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
    &lt;/button&gt;
    &lt;button class=&quot;button--secondary&quot;&gt;
        &lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt;
        Edit
    &lt;/button&gt;
    &lt;button class=&quot;button--danger&quot;&gt;
        &lt;i class=&quot;fa fa-trash-o&quot;&gt;&lt;/i&gt;
        Delete
    &lt;/button&gt;
    &lt;button class=&quot;button--cancel&quot;&gt;
        &lt;i class=&quot;fa fa-refresh&quot;&gt;&lt;/i&gt;
        Resume
    &lt;/button&gt;
&lt;/div&gt;
</pre></details>


<h3>9.3.7. Placeholders</h3>
<p>Placeholders provide the user with an example of the what the field should contain. Typically, include <em>e.g.</em> at the beginning. Do not use placeholder in place of labels.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>input</li><li>textarea</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><input type="text" placeholder="e.g. Placeholder" />
</div><details><summary>Code</summary><pre>&lt;input type=&quot;text&quot; placeholder=&quot;e.g. Placeholder&quot; /&gt;
</pre></details>


<h3>9.3.8. Text Inputs</h3>
<p>Range elements do not use sliders. Instead, ranges are input as two text fields.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>input</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>disabled</li><li>hover</li><li>focus</li><li>selected</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field form-field--text">
        <input type="text" placeholder="Example text input" />
    </div>

    <div class="form-field form-field--text form-field--disabled">
        <label>Disabled</label>
        <input type="text" placeholder="Example disabled" disabled="disabled" />
    </div>

    <div class="form-field form-field--text form-field--success">
        <label>Success</label>
        <input type="text" placeholder="Example success" />
        <span class="form-field__feedback">
            <i class="fa fa-check"></i>
            This is a success
        </span>
    </div>

    <div class="form-field form-field--text form-field--warning">
        <label>Warning</label>
        <input type="text" placeholder="Example warning" />
        <span class="form-field__feedback">
            <i class="fa fa-exclamation"></i>
            This is a warning
        </span>
    </div>

    <div class="form-field form-field--text form-field--error">
        <label>Error</label>
        <input type="text" placeholder="Example error" />
        <span class="form-field__feedback">
            <i class="fa fa-ban"></i>
            This is an error
        </span>
    </div>
</form>

<input type="email" placeholder="e.g. alice@example.com" />

<input type="number" placeholder="0" />

<input type="url" placeholder="e.g. https://google.com" />

<input type="time" step="1" />

<input type="search" placeholder="Search" />

<input type="search" placeholder="Search" autocomplete="off" />

<input type="tel" placeholder="e.g. 515-481-9182" />

<input type="password" />

<input type="number" placeholder="Min" />
<input type="number" placeholder="Max" />
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field form-field--text&quot;&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example text input&quot; /&gt;
    &lt;/div&gt;

    &lt;div class=&quot;form-field form-field--text form-field--disabled&quot;&gt;
        &lt;label&gt;Disabled&lt;/label&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example disabled&quot; disabled=&quot;disabled&quot; /&gt;
    &lt;/div&gt;

    &lt;div class=&quot;form-field form-field--text form-field--success&quot;&gt;
        &lt;label&gt;Success&lt;/label&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example success&quot; /&gt;
        &lt;span class=&quot;form-field__feedback&quot;&gt;
            &lt;i class=&quot;fa fa-check&quot;&gt;&lt;/i&gt;
            This is a success
        &lt;/span&gt;
    &lt;/div&gt;

    &lt;div class=&quot;form-field form-field--text form-field--warning&quot;&gt;
        &lt;label&gt;Warning&lt;/label&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example warning&quot; /&gt;
        &lt;span class=&quot;form-field__feedback&quot;&gt;
            &lt;i class=&quot;fa fa-exclamation&quot;&gt;&lt;/i&gt;
            This is a warning
        &lt;/span&gt;
    &lt;/div&gt;

    &lt;div class=&quot;form-field form-field--text form-field--error&quot;&gt;
        &lt;label&gt;Error&lt;/label&gt;
        &lt;input type=&quot;text&quot; placeholder=&quot;Example error&quot; /&gt;
        &lt;span class=&quot;form-field__feedback&quot;&gt;
            &lt;i class=&quot;fa fa-ban&quot;&gt;&lt;/i&gt;
            This is an error
        &lt;/span&gt;
    &lt;/div&gt;
&lt;/form&gt;

&lt;input type=&quot;email&quot; placeholder=&quot;e.g. alice@example.com&quot; /&gt;

&lt;input type=&quot;number&quot; placeholder=&quot;0&quot; /&gt;

&lt;input type=&quot;url&quot; placeholder=&quot;e.g. https://google.com&quot; /&gt;

&lt;input type=&quot;time&quot; step=&quot;1&quot; /&gt;

&lt;input type=&quot;search&quot; placeholder=&quot;Search&quot; /&gt;

&lt;input type=&quot;search&quot; placeholder=&quot;Search&quot; autocomplete=&quot;off&quot; /&gt;

&lt;input type=&quot;tel&quot; placeholder=&quot;e.g. 515-481-9182&quot; /&gt;

&lt;input type=&quot;password&quot; /&gt;

&lt;input type=&quot;number&quot; placeholder=&quot;Min&quot; /&gt;
&lt;input type=&quot;number&quot; placeholder=&quot;Max&quot; /&gt;
</pre></details>


<h3>9.3.9. Textarea</h3>
<p>Text areas are for larger text entry that a normal <code>input</code>.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>textarea</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><textarea cols="40" id="thoughts" name="thoughts" rows="4"></textarea>
</div><details><summary>Code</summary><pre>&lt;textarea cols=&quot;40&quot; id=&quot;thoughts&quot; name=&quot;thoughts&quot; rows=&quot;4&quot;&gt;&lt;/textarea&gt;
</pre></details>


<h3>9.3.10. Checkboxes and Radios</h3>
<p>Checkboxes and radios receive some special styling in Chrome and Safari.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>input</li><li>label</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>hover</li><li>selected</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul class="unstyled">
    <li>
        <label class="checkbox">
            <input type="checkbox" value="option1"> Option 1
        </label>
    </li>
    <li>
        <label class="checkbox">
            <input type="checkbox" value="option1"> Option 2
        </label>
    </li>
    <li>
        <label class="checkbox">
            <input type="checkbox" value="option1"> Option 3
        </label>
    </li>
</ul>

<label class="checkbox">
    <input type="checkbox" value="option1"> Option 1
</label>

<label class="toggle">
    <input type="checkbox" value="option1"> Option 1
</label>

<ul class="unstyled">
    <li>
        <label class="radio">
            <input type="radio" name="radio" value="option1"> Option 1
        </label>
    </li>
    <li>
        <label class="radio">
            <input type="radio" name="radio" value="option1"> Option 2
        </label>
    </li>
    <li>
        <label class="radio">
            <input type="radio" name="radio" value="option1"> Option 3
        </label>
    </li>
</ul>
</div><details><summary>Code</summary><pre>&lt;ul class=&quot;unstyled&quot;&gt;
    &lt;li&gt;
        &lt;label class=&quot;checkbox&quot;&gt;
            &lt;input type=&quot;checkbox&quot; value=&quot;option1&quot;&gt; Option 1
        &lt;/label&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;label class=&quot;checkbox&quot;&gt;
            &lt;input type=&quot;checkbox&quot; value=&quot;option1&quot;&gt; Option 2
        &lt;/label&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;label class=&quot;checkbox&quot;&gt;
            &lt;input type=&quot;checkbox&quot; value=&quot;option1&quot;&gt; Option 3
        &lt;/label&gt;
    &lt;/li&gt;
&lt;/ul&gt;

&lt;label class=&quot;checkbox&quot;&gt;
    &lt;input type=&quot;checkbox&quot; value=&quot;option1&quot;&gt; Option 1
&lt;/label&gt;

&lt;label class=&quot;toggle&quot;&gt;
    &lt;input type=&quot;checkbox&quot; value=&quot;option1&quot;&gt; Option 1
&lt;/label&gt;

&lt;ul class=&quot;unstyled&quot;&gt;
    &lt;li&gt;
        &lt;label class=&quot;radio&quot;&gt;
            &lt;input type=&quot;radio&quot; name=&quot;radio&quot; value=&quot;option1&quot;&gt; Option 1
        &lt;/label&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;label class=&quot;radio&quot;&gt;
            &lt;input type=&quot;radio&quot; name=&quot;radio&quot; value=&quot;option1&quot;&gt; Option 2
        &lt;/label&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;label class=&quot;radio&quot;&gt;
            &lt;input type=&quot;radio&quot; name=&quot;radio&quot; value=&quot;option1&quot;&gt; Option 3
        &lt;/label&gt;
    &lt;/li&gt;
&lt;/ul&gt;
</pre></details>


<h3>9.3.11. Select</h3>
<p>The select component, more often used than the native select, uses checkboxes and radios and smartly updates based on the number of options</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><span class="select">
    <ul class="unstyled">
        <li>
            <label>
                <input type="radio" value="post" name="kind">
                Post
            </label>
        </li>
        <li>
            <label>
                <input type="radio" value="proposal" name="kind">
                Proposal
            </label>
        </li>
        <li>
            <label>
                <input type="radio" value="vote" name="kind">
                Vote
            </label>
        </li>
        <li>
            <label>
                <input type="radio" value="flag" name="kind">
                Flag
            </label>
        </li>
    </ul>
</span>
</div><details><summary>Code</summary><pre>&lt;span class=&quot;select&quot;&gt;
    &lt;ul class=&quot;unstyled&quot;&gt;
        &lt;li&gt;
            &lt;label&gt;
                &lt;input type=&quot;radio&quot; value=&quot;post&quot; name=&quot;kind&quot;&gt;
                Post
            &lt;/label&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;label&gt;
                &lt;input type=&quot;radio&quot; value=&quot;proposal&quot; name=&quot;kind&quot;&gt;
                Proposal
            &lt;/label&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;label&gt;
                &lt;input type=&quot;radio&quot; value=&quot;vote&quot; name=&quot;kind&quot;&gt;
                Vote
            &lt;/label&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;label&gt;
                &lt;input type=&quot;radio&quot; value=&quot;flag&quot; name=&quot;kind&quot;&gt;
                Flag
            &lt;/label&gt;
        &lt;/li&gt;
    &lt;/ul&gt;
&lt;/span&gt;
</pre></details>


<h2>9.4. Grouped Inputs</h2>
<p>Grouped inputs are useful for data entry where the data points are very closely related. Otherwise, prefer to stick with one column forms.</p>

<h6 class="sg-field">Modifiers</h6>
<ul><li>--grouped</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form>
    <div class="form-field--grouped">
        <div class="form-field form-field--text">
            <label for="given-name">Given Name</label>
            <input id="given-name" name="given-name" placeholder="" size="20" type="text" />
        </div>
        <div class="form-field form-field--text">
            <label for="family-name">Family Name</label>
            <input id="family-name" name="family-name" placeholder="" size="20" type="text" />
        </div>
    </div>
</form>
</div><details><summary>Code</summary><pre>&lt;form&gt;
    &lt;div class=&quot;form-field--grouped&quot;&gt;
        &lt;div class=&quot;form-field form-field--text&quot;&gt;
            &lt;label for=&quot;given-name&quot;&gt;Given Name&lt;/label&gt;
            &lt;input id=&quot;given-name&quot; name=&quot;given-name&quot; placeholder=&quot;&quot; size=&quot;20&quot; type=&quot;text&quot; /&gt;
        &lt;/div&gt;
        &lt;div class=&quot;form-field form-field--text&quot;&gt;
            &lt;label for=&quot;family-name&quot;&gt;Family Name&lt;/label&gt;
            &lt;input id=&quot;family-name&quot; name=&quot;family-name&quot; placeholder=&quot;&quot; size=&quot;20&quot; type=&quot;text&quot; /&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/form&gt;
</pre></details>


<h2>9.5. Horizontal Forms</h2>
<p>Most of the time, the verical form is for the best. For small forms, it may be easier to lay them out horizontally. In this one case, it can be necessary to use placeholders as labels.</p>

<h6 class="sg-field">Modifiers</h6>
<ul><li>--horizontal</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><form class="form--horizontal">
    <div class="form-field form-field--search">
        <input id="name" name="name" placeholder="Search" size="20" type="search" />
    </div>
    <div class="form-field form-field--boolean">
        <label for="spam">
            <input name="spam" id="spam" type="checkbox" value="y">
            Include all types
        </label>
    </div>
    <button type="submit">
        <i class="fa fa-search"></i>
        Search
    </button>
</form>
</div><details><summary>Code</summary><pre>&lt;form class=&quot;form--horizontal&quot;&gt;
    &lt;div class=&quot;form-field form-field--search&quot;&gt;
        &lt;input id=&quot;name&quot; name=&quot;name&quot; placeholder=&quot;Search&quot; size=&quot;20&quot; type=&quot;search&quot; /&gt;
    &lt;/div&gt;
    &lt;div class=&quot;form-field form-field--boolean&quot;&gt;
        &lt;label for=&quot;spam&quot;&gt;
            &lt;input name=&quot;spam&quot; id=&quot;spam&quot; type=&quot;checkbox&quot; value=&quot;y&quot;&gt;
            Include all types
        &lt;/label&gt;
    &lt;/div&gt;
    &lt;button type=&quot;submit&quot;&gt;
        &lt;i class=&quot;fa fa-search&quot;&gt;&lt;/i&gt;
        Search
    &lt;/button&gt;
&lt;/form&gt;
</pre></details>


<h1>10. Tables</h1>
<p>Tables are zebra-striped, and common elements such as header and footer rows are available. Rows classes are available for each hue; as they only change hue, another indicator needs to be used to differentiate row types. Supplimental tags, such as <code>tbody</code> are recommended.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>table, caption, thead, tr, th, td, tfoot</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>row--accept</li><li>row--accent</li><li>row--error</li><li>row--warn</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><table> <caption>An example table with a header row and a caption.</caption> <thead> <tr> <th>ID</th> <th>Username</th> <th>Email</th> <th>Action</th> </tr> </thead> <tbody> <tr> <td>1</td> <td>Marissa</td> <td>marissa@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr> <td>2</td> <td>Edward</td> <td>edward@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr> <td>3</td> <td>Theo</td> <td>theo@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr> <td>4</td> <td>Jasmine</td> <td>jasmine@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--accept"> <td>5</td> <td>Jacob</td> <td>jacob@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--accept"> <td>6</td> <td>Alexander</td> <td>alexander@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--accent"> <td>7</td> <td>Cornelia</td> <td>cornelia@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--accent"> <td>8</td> <td>Sophie</td> <td>sophie@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--error"> <td>9</td> <td>Kadri</td> <td>kadri@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--error"> <td>10</td> <td>Dalton</td> <td>dalton@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--warn"> <td>13</td> <td>Iris</td> <td>iris@example.com</td> <td><a href="#">Contact</a></td> </tr> <tr class="row--warn"> <td>14</td> <td>Frederico</td> <td>frederico@example.com</td> <td><a href="#">Contact</a></td> </tr> </tbody> </table></div><details><summary>Code</summary><pre>&lt;table&gt; &lt;caption&gt;An example table with a header row and a caption.&lt;/caption&gt; &lt;thead&gt; &lt;tr&gt; &lt;th&gt;ID&lt;/th&gt; &lt;th&gt;Username&lt;/th&gt; &lt;th&gt;Email&lt;/th&gt; &lt;th&gt;Action&lt;/th&gt; &lt;/tr&gt; &lt;/thead&gt; &lt;tbody&gt; &lt;tr&gt; &lt;td&gt;1&lt;/td&gt; &lt;td&gt;Marissa&lt;/td&gt; &lt;td&gt;marissa@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr&gt; &lt;td&gt;2&lt;/td&gt; &lt;td&gt;Edward&lt;/td&gt; &lt;td&gt;edward@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr&gt; &lt;td&gt;3&lt;/td&gt; &lt;td&gt;Theo&lt;/td&gt; &lt;td&gt;theo@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr&gt; &lt;td&gt;4&lt;/td&gt; &lt;td&gt;Jasmine&lt;/td&gt; &lt;td&gt;jasmine@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--accept&quot;&gt; &lt;td&gt;5&lt;/td&gt; &lt;td&gt;Jacob&lt;/td&gt; &lt;td&gt;jacob@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--accept&quot;&gt; &lt;td&gt;6&lt;/td&gt; &lt;td&gt;Alexander&lt;/td&gt; &lt;td&gt;alexander@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--accent&quot;&gt; &lt;td&gt;7&lt;/td&gt; &lt;td&gt;Cornelia&lt;/td&gt; &lt;td&gt;cornelia@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--accent&quot;&gt; &lt;td&gt;8&lt;/td&gt; &lt;td&gt;Sophie&lt;/td&gt; &lt;td&gt;sophie@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--error&quot;&gt; &lt;td&gt;9&lt;/td&gt; &lt;td&gt;Kadri&lt;/td&gt; &lt;td&gt;kadri@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--error&quot;&gt; &lt;td&gt;10&lt;/td&gt; &lt;td&gt;Dalton&lt;/td&gt; &lt;td&gt;dalton@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--warn&quot;&gt; &lt;td&gt;13&lt;/td&gt; &lt;td&gt;Iris&lt;/td&gt; &lt;td&gt;iris@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;tr class=&quot;row--warn&quot;&gt; &lt;td&gt;14&lt;/td&gt; &lt;td&gt;Frederico&lt;/td&gt; &lt;td&gt;frederico@example.com&lt;/td&gt; &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Contact&lt;/a&gt;&lt;/td&gt; &lt;/tr&gt; &lt;/tbody&gt; &lt;/table&gt;</pre></details>


<h1>11. Components</h1>
<h2>11.1. Details & Summary</h2>
<p>Sometimes known as an accordian, the details and summary tags in HTML5 are somewhat styled.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>details</li><li>summary</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><details>
    <summary>More</summary>
    This is detailed information
</detail>
</div><details><summary>Code</summary><pre>&lt;details&gt;
    &lt;summary&gt;More&lt;/summary&gt;
    This is detailed information
&lt;/detail&gt;
</pre></details>


<h2>11.2. Alerts & Errors</h2>
<p>Systemic-alerts are often used when an error has occured. Alerts are fixed to the page until a user chooses to close them. Very serious alerts can force the user to reload the page. This situation calls for a modal.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>div (root)</li><li>a.alert__close</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>error</li><li>default</li><li>accept</li><li>accent</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><div class="alert--error">
    We are sorry, but an error has occurred. Please reload the page.
    <a href="#" class="alert__close">Close</a>
</div>

<div class="alert--default">
    We are sorry, but an error has occurred. Please reload the page.
    <a href="#" class="alert__close">Close</a>
</div>

<div class="alert--accept">
    We are sorry, but an error has occurred. Please reload the page.
    <a href="#" class="alert__close">Close</a>
</div>

<div class="alert--accent">
    We are sorry, but an error has occurred. Please reload the page.
    <a href="#" class="alert__close">Close</a>
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;alert--error&quot;&gt;
    We are sorry, but an error has occurred. Please reload the page.
    &lt;a href=&quot;#&quot; class=&quot;alert__close&quot;&gt;Close&lt;/a&gt;
&lt;/div&gt;

&lt;div class=&quot;alert--default&quot;&gt;
    We are sorry, but an error has occurred. Please reload the page.
    &lt;a href=&quot;#&quot; class=&quot;alert__close&quot;&gt;Close&lt;/a&gt;
&lt;/div&gt;

&lt;div class=&quot;alert--accept&quot;&gt;
    We are sorry, but an error has occurred. Please reload the page.
    &lt;a href=&quot;#&quot; class=&quot;alert__close&quot;&gt;Close&lt;/a&gt;
&lt;/div&gt;

&lt;div class=&quot;alert--accent&quot;&gt;
    We are sorry, but an error has occurred. Please reload the page.
    &lt;a href=&quot;#&quot; class=&quot;alert__close&quot;&gt;Close&lt;/a&gt;
&lt;/div&gt;
</pre></details>


<h2>11.3. Breadcrumbs, Wizards, & Pagination</h2>
<p>Breadcrumbs, wizards, and pagnition all server to help the user know where there are. Wizards and pagnition can also include linear forms of navigation.
TODO@ Don&#39;t require the Chevron list elements.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>nav - .breadcrumbs - .wizard - .pagnition</li><li>ol/ul, li, a</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><nav class="breadcrumbs">
    <ol>
        <li>
            <a href="#">
                Home
            </a>
        </li>
        <li><i class="fa fa-chevron-right"></i></li>
        <li>
            <a href="#">
                Learn
            </a>
        </li>
        <li><i class="fa fa-chevron-right"></i></li>
        <li>
            <a href="#">
                Propose
            </a>
        </li>
        <li><i class="fa fa-chevron-right"></i></li>
        <li class="selected">
            <a href="#">
                Analyze
            </a>
        </li>
    </ul>
</nav>


<nav class="wizard">
    <ol>
        <li>
            <a href="#">
                1.
                Home
            </a>
        </li>
        <li>
            <i class="fa fa-chevron-right"></i>
        </li>
        <li class="selected">
            <a href="#">
                2.
                Learn
            </a>
        </li>
        <li class="disabled">
            <i class="fa fa-chevron-right"></i>
        </li>
        <li class="disabled">
            <a href="#">
                3.
                Propose
            </a>
        </li>
        <li class="disabled">
            <i class="fa fa-chevron-right"></i>
        </li>
        <li class="disabled">
            <a href="#">
                4.
                Analyze
            </a>
        </li>
    </ol>
</nav>

<nav class="pagination">
    <ul>
        <li>
            <a href="#">
                <i class="fa fa-chevron-left"></i>
                Back
            </a>
        </li>
        <li class="selected">
            <a href="#">1</a>
        </li>
        <li>
            <a href="#">2</a>
        </li>
        <li class="pagination__separator">&hellip;</li>
        <li>
            <a href="#">11</a>
        </li>
        <li>
            <a href="#">12</a>
        </li>
        <li>
            <a href="#">
                Next
                <i class="fa fa-chevron-right"></i>
            </a>
        </li>
    </ul>
</nav>
</div><details><summary>Code</summary><pre>&lt;nav class=&quot;breadcrumbs&quot;&gt;
    &lt;ol&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                Home
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;&lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;&lt;/li&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                Learn
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;&lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;&lt;/li&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                Propose
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;&lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;&lt;/li&gt;
        &lt;li class=&quot;selected&quot;&gt;
            &lt;a href=&quot;#&quot;&gt;
                Analyze
            &lt;/a&gt;
        &lt;/li&gt;
    &lt;/ul&gt;
&lt;/nav&gt;


&lt;nav class=&quot;wizard&quot;&gt;
    &lt;ol&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                1.
                Home
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
        &lt;/li&gt;
        &lt;li class=&quot;selected&quot;&gt;
            &lt;a href=&quot;#&quot;&gt;
                2.
                Learn
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li class=&quot;disabled&quot;&gt;
            &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
        &lt;/li&gt;
        &lt;li class=&quot;disabled&quot;&gt;
            &lt;a href=&quot;#&quot;&gt;
                3.
                Propose
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li class=&quot;disabled&quot;&gt;
            &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
        &lt;/li&gt;
        &lt;li class=&quot;disabled&quot;&gt;
            &lt;a href=&quot;#&quot;&gt;
                4.
                Analyze
            &lt;/a&gt;
        &lt;/li&gt;
    &lt;/ol&gt;
&lt;/nav&gt;

&lt;nav class=&quot;pagination&quot;&gt;
    &lt;ul&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                &lt;i class=&quot;fa fa-chevron-left&quot;&gt;&lt;/i&gt;
                Back
            &lt;/a&gt;
        &lt;/li&gt;
        &lt;li class=&quot;selected&quot;&gt;
            &lt;a href=&quot;#&quot;&gt;1&lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;2&lt;/a&gt;
        &lt;/li&gt;
        &lt;li class=&quot;pagination__separator&quot;&gt;&amp;hellip;&lt;/li&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;11&lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;12&lt;/a&gt;
        &lt;/li&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                Next
                &lt;i class=&quot;fa fa-chevron-right&quot;&gt;&lt;/i&gt;
            &lt;/a&gt;
        &lt;/li&gt;
    &lt;/ul&gt;
&lt;/nav&gt;
</pre></details>


<h2>11.4. Discussion</h2>
<p>Discussions are common on just about any social site. A default layout helps to bring consistency to these discussions. Discussions can also be modified to achieve the goal of the widget.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><ul class="discussion">
    <li>
        <div class="discussion__avatar">
            <img src="https://placekitten.com/g/48/48" data-title="username" />
        </div>
        <div class="discussion__content">
            <div class="discussion__when">
                52 minutes ago
            </div>
            <div class="discussion__name">
                username
            </div>
            <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.
            </p>
            <div class="discussion__footer">
                <a href="#"><i class="fa fa-edit"></i> Edit</a>
                <a href="#"><i class="fa fa-share"></i> Share</a>
                <a href="#"><i class="fa fa-flag"></i> Flag</a>
            </div>
        </div>
    </li>
    <li>
        <div class="discussion__avatar">
            <img src="https://placekitten.com/g/48/48" data-title="username" />
        </div>
        <div class="discussion__content">
            <div class="discussion__when">
                54 minutes ago
            </div>
            <div class="discussion__name">
                username
            </div>
            <p>
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.
            </p>
            <div class="discussion__footer">
                <a href="#"><i class="fa fa-edit"></i> Edit</a>
                <a href="#"><i class="fa fa-share"></i> Share</a>
                <a href="#"><i class="fa fa-flag"></i> Flag</a>
            </div>
        </div>
    </li>
</ul>
<hr />
<table class="discussion-list">
    <thead>
        <tr>
            <th>Topic</th>
            <th>Posts</th>
            <th>Views</th>
            <th>Last Modified</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td><a href="#">Astronomy set too large</a></td>
            <td>10</td>
            <td>45</td>
            <td>4 hours ago</td>
        </tr>
        <tr>
            <td><a href="#">Split up astronomy set</a></td>
            <td>15</td>
            <td>105</td>
            <td>2 hours ago</td>
        </tr>
    </tbody>
</table>
</div><details><summary>Code</summary><pre>&lt;ul class=&quot;discussion&quot;&gt;
    &lt;li&gt;
        &lt;div class=&quot;discussion__avatar&quot;&gt;
            &lt;img src=&quot;https://placekitten.com/g/48/48&quot; data-title=&quot;username&quot; /&gt;
        &lt;/div&gt;
        &lt;div class=&quot;discussion__content&quot;&gt;
            &lt;div class=&quot;discussion__when&quot;&gt;
                52 minutes ago
            &lt;/div&gt;
            &lt;div class=&quot;discussion__name&quot;&gt;
                username
            &lt;/div&gt;
            &lt;p&gt;
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.
            &lt;/p&gt;
            &lt;div class=&quot;discussion__footer&quot;&gt;
                &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt; Edit&lt;/a&gt;
                &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-share&quot;&gt;&lt;/i&gt; Share&lt;/a&gt;
                &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-flag&quot;&gt;&lt;/i&gt; Flag&lt;/a&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/li&gt;
    &lt;li&gt;
        &lt;div class=&quot;discussion__avatar&quot;&gt;
            &lt;img src=&quot;https://placekitten.com/g/48/48&quot; data-title=&quot;username&quot; /&gt;
        &lt;/div&gt;
        &lt;div class=&quot;discussion__content&quot;&gt;
            &lt;div class=&quot;discussion__when&quot;&gt;
                54 minutes ago
            &lt;/div&gt;
            &lt;div class=&quot;discussion__name&quot;&gt;
                username
            &lt;/div&gt;
            &lt;p&gt;
                Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
                tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,
                quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo.
            &lt;/p&gt;
            &lt;div class=&quot;discussion__footer&quot;&gt;
                &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-edit&quot;&gt;&lt;/i&gt; Edit&lt;/a&gt;
                &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-share&quot;&gt;&lt;/i&gt; Share&lt;/a&gt;
                &lt;a href=&quot;#&quot;&gt;&lt;i class=&quot;fa fa-flag&quot;&gt;&lt;/i&gt; Flag&lt;/a&gt;
            &lt;/div&gt;
        &lt;/div&gt;
    &lt;/li&gt;
&lt;/ul&gt;
&lt;hr /&gt;
&lt;table class=&quot;discussion-list&quot;&gt;
    &lt;thead&gt;
        &lt;tr&gt;
            &lt;th&gt;Topic&lt;/th&gt;
            &lt;th&gt;Posts&lt;/th&gt;
            &lt;th&gt;Views&lt;/th&gt;
            &lt;th&gt;Last Modified&lt;/th&gt;
        &lt;/tr&gt;
    &lt;/thead&gt;
    &lt;tbody&gt;
        &lt;tr&gt;
            &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Astronomy set too large&lt;/a&gt;&lt;/td&gt;
            &lt;td&gt;10&lt;/td&gt;
            &lt;td&gt;45&lt;/td&gt;
            &lt;td&gt;4 hours ago&lt;/td&gt;
        &lt;/tr&gt;
        &lt;tr&gt;
            &lt;td&gt;&lt;a href=&quot;#&quot;&gt;Split up astronomy set&lt;/a&gt;&lt;/td&gt;
            &lt;td&gt;15&lt;/td&gt;
            &lt;td&gt;105&lt;/td&gt;
            &lt;td&gt;2 hours ago&lt;/td&gt;
        &lt;/tr&gt;
    &lt;/tbody&gt;
&lt;/table&gt;
</pre></details>


<h3>11.4.1. Proposal</h3>
<p>A proposal to create, update, delete, merge, or split an entity.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="proposal">
    <div class="proposal__avatar">
        <img src="https://placekitten.com/g/48/48" data-title="username" />
    </div>
    <div class="proposal__content">
        <div class="proposal__when">
            3 hours ago
        </div>
        <div class="proposal__name">
            username
        </div>
        <p class="proposal__subject">
            Kind: Object Name
            <span class="proposal__action--update">Update</span>
            <span class="proposal__status--pending">Pending</span>
        </p>
        <div class="proposal__body">
            <p>
                Changes block TBD.
            </p>
        </div>
    </div>
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;proposal&quot;&gt;
    &lt;div class=&quot;proposal__avatar&quot;&gt;
        &lt;img src=&quot;https://placekitten.com/g/48/48&quot; data-title=&quot;username&quot; /&gt;
    &lt;/div&gt;
    &lt;div class=&quot;proposal__content&quot;&gt;
        &lt;div class=&quot;proposal__when&quot;&gt;
            3 hours ago
        &lt;/div&gt;
        &lt;div class=&quot;proposal__name&quot;&gt;
            username
        &lt;/div&gt;
        &lt;p class=&quot;proposal__subject&quot;&gt;
            Kind: Object Name
            &lt;span class=&quot;proposal__action--update&quot;&gt;Update&lt;/span&gt;
            &lt;span class=&quot;proposal__status--pending&quot;&gt;Pending&lt;/span&gt;
        &lt;/p&gt;
        &lt;div class=&quot;proposal__body&quot;&gt;
            &lt;p&gt;
                Changes block TBD.
            &lt;/p&gt;
        &lt;/div&gt;
    &lt;/div&gt;
&lt;/div&gt;
</pre></details>


<h3>11.4.2. Vote</h3>
<p>A vote from a user on a proposal.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="vote">
    <div class="vote__header">
        <span class="vote__action--consent">Consent</span>
        by
        <img src="https://placekitten.com/g/24/24" data-title="username" />
        <span class="vote__name">
            username
        </span>
        <span class="vote__when">
            3 hours ago
        </span>
    </div>
    <div class="vote__body">
        <p>
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt.
        </p>
    </div>
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;vote&quot;&gt;
    &lt;div class=&quot;vote__header&quot;&gt;
        &lt;span class=&quot;vote__action--consent&quot;&gt;Consent&lt;/span&gt;
        by
        &lt;img src=&quot;https://placekitten.com/g/24/24&quot; data-title=&quot;username&quot; /&gt;
        &lt;span class=&quot;vote__name&quot;&gt;
            username
        &lt;/span&gt;
        &lt;span class=&quot;vote__when&quot;&gt;
            3 hours ago
        &lt;/span&gt;
    &lt;/div&gt;
    &lt;div class=&quot;vote__body&quot;&gt;
        &lt;p&gt;
            Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod
            tempor incididunt.
        &lt;/p&gt;
    &lt;/div&gt;
&lt;/div&gt;
</pre></details>


<h2>11.5. Notice</h2>
<p>TBD</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><ul class="notices">
    <li class="notice notice--unread">
        <span class="notice__when">
            52 minutes ago
        </span>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit,
        sed do eiusmod tempor incididunt. <a href="#">Do something</a>.
    </li>
    <li class="notice">
        <span class="notice__when">
            3 hours ago
        </span>
        Lorem ipsum dolor sit amet, consectetur adipisicing elit,
        sed do eiusmod tempor incididunt. <a href="#">Do something</a>.
    </li>
</ul>
</div><details><summary>Code</summary><pre>&lt;ul class=&quot;notices&quot;&gt;
    &lt;li class=&quot;notice notice--unread&quot;&gt;
        &lt;span class=&quot;notice__when&quot;&gt;
            52 minutes ago
        &lt;/span&gt;
        Lorem ipsum dolor sit amet, consectetur adipisicing elit,
        sed do eiusmod tempor incididunt. &lt;a href=&quot;#&quot;&gt;Do something&lt;/a&gt;.
    &lt;/li&gt;
    &lt;li class=&quot;notice&quot;&gt;
        &lt;span class=&quot;notice__when&quot;&gt;
            3 hours ago
        &lt;/span&gt;
        Lorem ipsum dolor sit amet, consectetur adipisicing elit,
        sed do eiusmod tempor incididunt. &lt;a href=&quot;#&quot;&gt;Do something&lt;/a&gt;.
    &lt;/li&gt;
&lt;/ul&gt;
</pre></details>


<h2>11.6. Inline Labels</h2>
<p>Labels are available in each of the basic hues. It is typically used for numbers or to draw unique emphasis to words or short phrases.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>span (root)</li></ul>
<h6 class="sg-field">Modifiers</h6>
<ul><li>error</li><li>warn</li><li>accept</li><li>info</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><ul>
    <li>Error or Danger: <span class="label--error">label</span> and numeric label: <span class="label--error">100</span></li>
    <li>Default, Base or Warn: <span class="label--warn">label</span> and numeric label: <span class="label--warn">100</span></li>
    <li>Success or Accept: <span class="label--accept">label</span> and numeric label: <span class="label--accept">100</span></li>
    <li>Accent or Info: <span class="label--info">label</span> and numeric label: <span class="label--info">100</span></li>
</ul>
</div><details><summary>Code</summary><pre>&lt;ul&gt;
    &lt;li&gt;Error or Danger: &lt;span class=&quot;label--error&quot;&gt;label&lt;/span&gt; and numeric label: &lt;span class=&quot;label--error&quot;&gt;100&lt;/span&gt;&lt;/li&gt;
    &lt;li&gt;Default, Base or Warn: &lt;span class=&quot;label--warn&quot;&gt;label&lt;/span&gt; and numeric label: &lt;span class=&quot;label--warn&quot;&gt;100&lt;/span&gt;&lt;/li&gt;
    &lt;li&gt;Success or Accept: &lt;span class=&quot;label--accept&quot;&gt;label&lt;/span&gt; and numeric label: &lt;span class=&quot;label--accept&quot;&gt;100&lt;/span&gt;&lt;/li&gt;
    &lt;li&gt;Accent or Info: &lt;span class=&quot;label--info&quot;&gt;label&lt;/span&gt; and numeric label: &lt;span class=&quot;label--info&quot;&gt;100&lt;/span&gt;&lt;/li&gt;
&lt;/ul&gt;
</pre></details>


<h2>11.7. Audio, Video, & Embedded Objects</h2>
<p>Sagefy uses YouTube, Vimeo, Soundcloud, Slideshare, and third party resources to render media elements. These elements are embedded by a simple <code>iframe</code> tag, with no customization other than size.</p>

<h6 class="sg-field">Elements</h6>
<ul><li>audio, video, object, iframe</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example">TODO
</div><details><summary>Code</summary><pre>TODO
</pre></details>


<h2>11.8. Menu</h2>
<p>Sagefy&#39;s most common navigational element is a simple menu. The user clicks on the Sagefy icon, and a pane of menu options provides the user with more functionality. This helps to prevent cognitive overload.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="menu">
    <div class="menu__overlay"></div>
    <a href="#" class="menu__trigger">
        <div class="menu__logo"></div>
        <i class="menu__close fa fa-times-circle" style="display:none"></i>
    </a>
    <a href="#" class="menu__close"></a>
    <ul class="menu_items">
        <li>
            <a href="#">
                <i class="fa fa-square"></i>
                <div class="menu__item__title">
                    Menu Item
                </div>
            </a>
        </li>
    </ul>
</div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;menu&quot;&gt;
    &lt;div class=&quot;menu__overlay&quot;&gt;&lt;/div&gt;
    &lt;a href=&quot;#&quot; class=&quot;menu__trigger&quot;&gt;
        &lt;div class=&quot;menu__logo&quot;&gt;&lt;/div&gt;
        &lt;i class=&quot;menu__close fa fa-times-circle&quot; style=&quot;display:none&quot;&gt;&lt;/i&gt;
    &lt;/a&gt;
    &lt;a href=&quot;#&quot; class=&quot;menu__close&quot;&gt;&lt;/a&gt;
    &lt;ul class=&quot;menu_items&quot;&gt;
        &lt;li&gt;
            &lt;a href=&quot;#&quot;&gt;
                &lt;i class=&quot;fa fa-square&quot;&gt;&lt;/i&gt;
                &lt;div class=&quot;menu__item__title&quot;&gt;
                    Menu Item
                &lt;/div&gt;
            &lt;/a&gt;
        &lt;/li&gt;
    &lt;/ul&gt;
&lt;/div&gt;
</pre></details>


<h2>11.9. Progressbars</h2>
<p>For progress bars, use the <code>progress</code> tag.</p>
<p>TODO Design and style</p>

<h6 class="sg-field">Elements</h6>
<ul><li>progress - span</li></ul>
<h6 class="sg-field">Example</h6><div class="sg-example"><progress max="70"><span>0</span>%</progress>
</div><details><summary>Code</summary><pre>&lt;progress max=&quot;70&quot;&gt;&lt;span&gt;0&lt;/span&gt;%&lt;/progress&gt;
</pre></details>


<h2>11.10. Spinners</h2>
<p>A placeholder element to wait for things to load.</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><div class="spinner"></div>
</div><details><summary>Code</summary><pre>&lt;div class=&quot;spinner&quot;&gt;&lt;/div&gt;
</pre></details>


<h2>11.11. Tooltips</h2>
<p>Hover over an element with <code>data-title</code> to view the contents. No JavaScript required!</p>

<h6 class="sg-field">Example</h6><div class="sg-example"><a href="#" data-title="Auto tooltip">An example</a> of a tooltip
</div><details><summary>Code</summary><pre>&lt;a href=&quot;#&quot; data-title=&quot;Auto tooltip&quot;&gt;An example&lt;/a&gt; of a tooltip
</pre></details>


<h1>12. More Remarks</h1>
<h3 id="extending-with-bem">Extending with BEM</h3>
<p>Non-tag elements in the Sagefy ecosystem use the <a href="http://csswizardry.com/2013/01/mindbemding-getting-your-head-round-bem-syntax/">BEM syntax</a>.</p>
<h3 id="additions">Additions</h3>
<p>Prefer to add components to the general styleguide than inventing new components for specific interfaces. Reuse ensures code maintainability and efficiency.</p>
<h3 id="browser-support">Browser Support</h3>
<p>At this time, Sagefy supports Firefox, Chrome, &amp; Safari, at the latest consumer version and the latest immediately-previous major consumer version. As of <time>2014 April 29</time>:</p>
<ul>
<li><strong>Firefox</strong>: 29, 28</li>
<li><strong>Chrome</strong>: 34, 33</li>
<li><strong>Safari</strong>: 7, 6</li>
</ul>
<h3 id="even-more-todo-">Even More TODO...</h3>
<ul>
<li>Code syntax highlighting</li>
<li>Uploading images</li>
</ul>




"""

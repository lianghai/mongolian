<hgroup>
  <p>Draft technical note:</p>
  <h1>Text representation and shaping specification of the Mongolian script</h1>
</hgroup>

<p>
  This <em>draft</em> specification demonstrates and proposes how to specify both
  comprehensive guidelines for text representation and coherent rules for text shaping.
  It mainly deals with the first three layers in the overall technical architecture
  of rendering texts in the Mongolian script:
</p>

<ul>
  <li>
    The Unicode Standard and ISO/IEC 10646, a synchronized pair of standards,
    specify identities of encoded characters and standardized variation
    sequences.
  </li>
  <li>
    The Unicode Standard and its various supplementary standards further provide
    the characters with additional behavioral specifications, including
    character properties (general category, cursive joining type, etc.) and
    algorithms (normalization, collation, line breaking, text segmentation,
    bidirectional, vertical text layout, etc.).
  </li>
  <li>
    The required complex shaping is implemented in fonts and text shaping
    engines, according to OpenType Layout (OTL) or other complex shaping models,
    such as AAT (Apple Advanced Typography) and Graphite.
  </li>
  <li>
    Hudum text is treated inline as horizontal and left-to-right, while text
    layout engines are responsible for setting lines vertically and arranging
    multiple lines with the preferred left-to-right order.
  </li>
</ul>

<p>
  Although the architectural defects cannot be resolved without migrating to a
  radically different encoding model, a meticulous specification can help
  eliminate unwanted differences between vendor implementations.
</p>

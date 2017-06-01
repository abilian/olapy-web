from __future__ import absolute_import, division, print_function

import six


class IFrame(object):
    """Frame in which we can drag and drop our columns."""

    iframe = """
        <iframe
            width="{width}"
            height="{height}"
            src="{src}{params}"
            frameborder="0"
            allowfullscreen
        ></iframe>
        """

    def __init__(self, src, width, height, **kwargs):
        """
        Iframe
        :param src:
        :param width:
        :param height:
        :param kwargs:
        """
        self.src = src
        self.width = width
        self.height = height
        self.params = kwargs

    def _repr_html_(self):
        """return the embed iframe."""
        if self.params:
            # try:
            #     from urllib.parse import urlencode  # Py 3
            # except ImportError:

            params = "?" + six.moves.urllib.parse.urlencode(self.params)
        else:
            params = ""
        return self.iframe.format(
            src=self.src, width=self.width, height=self.height, params=params)


template = """
<!DOCTYPE html>
<html>
    <head>
        <title>PivotTable.js</title>

        <!-- external libs from cdnjs -->
        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.css">
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jqueryui/1.11.4/jquery-ui.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/d3/3.5.5/d3.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/jquery-csv/0.71/jquery.csv-0.71.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/c3/0.4.10/c3.min.js"></script>

        <link rel="stylesheet" type="text/css" href="https://cdnjs.cloudflare.com/ajax/libs/pivottable/1.6.3/pivot.min.css">
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/1.6.3/pivot.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/1.6.3/d3_renderers.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/1.6.3/c3_renderers.min.js"></script>
        <script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/pivottable/1.6.3/export_renderers.min.js"></script>

        <style>
            body {font-family: Verdana;}
            .node {
              border: solid 1px white;
              font: 10px sans-serif;
              line-height: 12px;
              overflow: hidden;
              position: absolute;
              text-indent: 2px;
            }
            .c3-line, .c3-focused {stroke-width: 3px !important;}
            .c3-bar {stroke: white !important; stroke-width: 1;}
            .c3 text { font-size: 12px; color: grey;}
            .tick line {stroke: white;}
            .c3-axis path {stroke: grey;}
            .c3-circle { opacity: 1 !important; }
        </style>
    </head>
    <body>
        <script type="text/javascript">
            $(function(){
                if(window.location != window.parent.location)
                    $("<a>", {target:"_blank", href:""})
                        .text("[pop out]").prependTo($("body"));

                $("#output").pivotUI(
                    $.csv.toArrays($("#output").text()),
                    {
                        renderers: $.extend(
                            $.pivotUtilities.renderers,
                            $.pivotUtilities.c3_renderers,
                            $.pivotUtilities.d3_renderers,
                            $.pivotUtilities.export_renderers
                            ),
                        hiddenAttributes: [""]
                    }
                ).show();
             });
        </script>
        <div id="output" style="display: none;">%s</div>
    </body>
</html>
"""


def pivot_ui(df, outfile_path="pivottablejs.html", width="100%", height="500"):
    """
    Create pivot table html page relative to DataFrame.

    :param df: the DataFrame
    :param outfile_path: html page name (can be the path also)
    :param width: page width
    :param height: page height
    :return: IFrame (html page) that can be injected to other html page
    """
    with open(outfile_path, 'w') as outfile:
        outfile.write(template % df.to_csv(encoding="utf-8"))
    return IFrame(src=outfile_path, width=width, height=height)

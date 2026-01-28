from platform import node
import re
from textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    res = []
    for node in old_nodes:
        if node.text_type is not TextType.TEXT:
            res.append(node)
            continue
        new_nodes = []
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise Exception("Invalid markdown syntax")
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(parts[i], text_type))
        res.extend(new_nodes)
    return res


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def split_nodes_image(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        text = node.text
        matches = extract_markdown_images(node.text)
        if len(matches) == 0:
            res.append(node)
            continue

        for alt, url in matches:
            parts = text.split(f"![{alt}]({url})", 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if parts[0] != "":
                res.append(TextNode(parts[0], TextType.TEXT))
            res.append(TextNode(alt, TextType.IMAGE, url))
            text = parts[1]
        if text != "":
            res.append(TextNode(text, TextType.TEXT))
    return res


def split_nodes_link(old_nodes):
    res = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            res.append(node)
            continue

        text = node.text
        matches = extract_markdown_links(node.text)
        if len(matches) == 0:
            res.append(node)
            continue

        for alt, url in matches:
            parts = text.split(f"[{alt}]({url})", 1)
            if len(parts) != 2:
                raise ValueError("invalid markdown, image section not closed")
            if parts[0] != "":
                res.append(TextNode(parts[0], TextType.TEXT))
            res.append(TextNode(alt, TextType.LINK, url))
            text = parts[1]
        if text != "":
            res.append(TextNode(text, TextType.TEXT))
    return res


def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes
